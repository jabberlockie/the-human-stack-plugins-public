#!/usr/bin/env python3
"""
Session Hoardinator — JSONL Session Parser

Parses Claude Code JSONL session transcripts and generates SQL INSERT
statements for Supabase upload.

Usage:
    python3 parse-sessions.py [options]

Options:
    --session <session-id>    Parse single session (for /log)
    --project-dir <path>      Project directory for namespace (default: cwd)
    --output <dir>            Output directory for SQL files (default: /tmp/hoardinator-sql/)
    --dry-run                 Count only, don't write SQL
    --sessions-dir <path>     Override ~/.claude/projects/ scan path
    --incremental <json>      JSON with existing session states from DB for delta detection

No external dependencies -- stdlib only.
"""

import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BATCH_SIZE = 40
CONTENT_TRUNCATE = 2000
SUMMARY_TRUNCATE = 500

SKIP_TYPES = {"progress", "file-history-snapshot", "queue-operation"}
PROCESS_TYPES = {"user", "assistant", "system"}

TOOL_CATEGORIES = {
    "Read": "file",
    "Write": "file",
    "Edit": "file",
    "Glob": "file",
    "Grep": "file",
    "NotebookEdit": "file",
    "Bash": "bash",
    "Task": "agent",
    "Skill": "skill",
    "WebFetch": "web",
    "AskUserQuestion": "interaction",
    "TodoWrite": "todo",
    "ToolSearch": "tool_search",
}

SENSITIVE_FILE_PATTERNS = re.compile(
    r"(\.env|\.pem|\.key|credentials|secrets|token)", re.IGNORECASE
)

SECRET_PATTERNS = re.compile(
    r"(sk-[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9\-_.]+|AKIA[A-Z0-9]{16}|ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|xox[bps]-[A-Za-z0-9\-]+)"
)

DESTRUCTIVE_PATTERNS = re.compile(
    r"(rm\s+-rf\b|DROP\s|--force\b|git\s+reset\s+--hard|git\s+push\s+--force)"
)

# Infra tool heuristics: commands that are git/npm/docker/infra tasks
INFRA_COMMAND_PATTERNS = re.compile(
    r"^\s*(git\s|npm\s|npx\s|yarn\s|pnpm\s|docker\s|pip\s|pip3\s|brew\s|apt\s|curl\s|wget\s)"
)

# ---------------------------------------------------------------------------
# Dollar-quoting
# ---------------------------------------------------------------------------


def dollar_quote(value):
    """Wrap a string value in PostgreSQL dollar-quoting.

    Uses $hd$...$hd$ by default.  If the content contains $hd$, falls back
    to $hd2$...$hd2$.
    """
    if value is None:
        return "NULL"
    s = str(value)
    if "$hd$" not in s:
        return f"$hd${s}$hd$"
    if "$hd2$" not in s:
        return f"$hd2${s}$hd2$"
    # Extremely unlikely: both tags present, strip the tag from content
    s = s.replace("$hd2$", "")
    return f"$hd2${s}$hd2$"


def sql_value(value):
    """Convert a Python value to a SQL literal."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, list):
        # text[] array
        elements = ", ".join(dollar_quote(v) for v in value)
        return f"ARRAY[{elements}]::text[]"
    return dollar_quote(value)


def sql_array_or_empty(lst):
    """Return ARRAY[...] or ARRAY[]::text[] for empty lists."""
    if not lst:
        return "ARRAY[]::text[]"
    elements = ", ".join(dollar_quote(v) for v in lst)
    return f"ARRAY[{elements}]::text[]"


# ---------------------------------------------------------------------------
# Truncation helpers
# ---------------------------------------------------------------------------


def truncate(text, max_len=CONTENT_TRUNCATE):
    """Truncate text to max_len characters."""
    if text is None:
        return None
    s = str(text)
    if len(s) <= max_len:
        return s
    return s[:max_len]


def summarize_input(tool_name, input_obj):
    """Create a human-readable summary of tool input."""
    if not isinstance(input_obj, dict):
        return truncate(str(input_obj), SUMMARY_TRUNCATE)

    parts = []
    if tool_name == "Bash":
        cmd = input_obj.get("command", "")
        desc = input_obj.get("description", "")
        if desc:
            parts.append(desc)
        else:
            parts.append(cmd)
    elif tool_name == "Read":
        parts.append(input_obj.get("file_path", ""))
    elif tool_name in ("Write", "Edit"):
        parts.append(input_obj.get("file_path", ""))
    elif tool_name == "Glob":
        parts.append(input_obj.get("pattern", ""))
    elif tool_name == "Grep":
        parts.append(input_obj.get("pattern", ""))
        path = input_obj.get("path", "")
        if path:
            parts.append(f"in {path}")
    elif tool_name == "WebFetch":
        parts.append(input_obj.get("url", ""))
    elif tool_name == "Task":
        parts.append(input_obj.get("description", ""))
    elif tool_name == "Skill":
        parts.append(input_obj.get("skill", ""))
    elif tool_name == "NotebookEdit":
        parts.append(input_obj.get("notebook_path", ""))
    elif tool_name == "TodoWrite":
        todos = input_obj.get("todos", [])
        parts.append(f"{len(todos)} todos")
    else:
        # For MCP and other tools, take the first few key=value pairs
        for k, v in list(input_obj.items())[:3]:
            sv = str(v)
            if len(sv) > 100:
                sv = sv[:100] + "..."
            parts.append(f"{k}={sv}")

    return truncate(" ".join(parts), SUMMARY_TRUNCATE)


def summarize_output(tool_name, tool_use_result):
    """Create a human-readable summary of tool output."""
    if tool_use_result is None:
        return None

    if isinstance(tool_use_result, str):
        return truncate(tool_use_result, SUMMARY_TRUNCATE)

    if isinstance(tool_use_result, list):
        return truncate(json.dumps(tool_use_result, default=str)[:SUMMARY_TRUNCATE], SUMMARY_TRUNCATE)

    if not isinstance(tool_use_result, dict):
        return truncate(str(tool_use_result), SUMMARY_TRUNCATE)

    parts = []
    # Bash
    stdout = tool_use_result.get("stdout")
    stderr = tool_use_result.get("stderr")
    if stdout:
        parts.append(truncate(stdout, 200))
    if stderr:
        parts.append(f"STDERR: {truncate(stderr, 200)}")

    # File operations
    file_path = tool_use_result.get("filePath")
    if file_path:
        parts.append(f"file: {file_path}")

    # Glob
    num_files = tool_use_result.get("numFiles")
    if num_files is not None:
        parts.append(f"{num_files} files")

    # Grep
    matches = tool_use_result.get("matches")
    if matches is not None:
        if isinstance(matches, list):
            parts.append(f"{len(matches)} matches")

    # content field
    content = tool_use_result.get("content")
    if content and not parts:
        if isinstance(content, str):
            parts.append(truncate(content, 200))
        elif isinstance(content, list):
            parts.append(f"{len(content)} blocks")

    # message/status
    msg = tool_use_result.get("message")
    if msg and not parts:
        parts.append(truncate(msg, 200))

    status = tool_use_result.get("status")
    if status and not parts:
        parts.append(status)

    if not parts:
        return truncate(json.dumps(tool_use_result, default=str), SUMMARY_TRUNCATE)

    return truncate("; ".join(parts), SUMMARY_TRUNCATE)


# ---------------------------------------------------------------------------
# Tool classification
# ---------------------------------------------------------------------------


def classify_tool(tool_name):
    """Return the tool category for a given tool name."""
    if tool_name in TOOL_CATEGORIES:
        return TOOL_CATEGORIES[tool_name]
    if tool_name.startswith("mcp__"):
        return "plugin"
    return "other"


def extract_plugin_name(tool_name):
    """Extract the plugin name from an MCP tool name.

    mcp__plugin_supabase_supabase__execute_sql -> supabase
    mcp__playwright__navigate -> playwright
    """
    if not tool_name.startswith("mcp__"):
        return None
    # Strip mcp__ prefix
    rest = tool_name[5:]
    # Try plugin_<name>_ pattern first
    m = re.match(r"plugin_([^_]+)_", rest)
    if m:
        return m.group(1)
    # Otherwise take the first segment
    parts = rest.split("__")
    if parts:
        return parts[0]
    return None


# ---------------------------------------------------------------------------
# Security detection
# ---------------------------------------------------------------------------


def is_sensitive_file(path):
    """Check if a file path matches sensitive file patterns."""
    if not path:
        return False
    return bool(SENSITIVE_FILE_PATTERNS.search(path))


def has_secret_exposure(text):
    """Check if text contains potential secret patterns."""
    if not text:
        return False
    return bool(SECRET_PATTERNS.search(str(text)))


def is_destructive_command(text):
    """Check if text contains destructive command patterns."""
    if not text:
        return False
    return bool(DESTRUCTIVE_PATTERNS.search(str(text)))


def is_infra_command(command_text):
    """Check if a bash command is infra-related (git, npm, docker, etc.)."""
    if not command_text:
        return False
    return bool(INFRA_COMMAND_PATTERNS.match(str(command_text)))


# ---------------------------------------------------------------------------
# Namespace derivation
# ---------------------------------------------------------------------------


def derive_namespace(project_dir):
    """Derive repo, org, and author from git remote and config."""
    repo = ""
    org = ""
    author = ""

    try:
        remote_url = subprocess.check_output(
            ["git", "-C", project_dir, "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        # Strip github.com prefix in both SSH and HTTPS formats
        # SSH:   git@github.com:org/repo.git
        # HTTPS: https://github.com/org/repo.git
        remote_url = re.sub(r".*github\.com[:/]", "", remote_url)
        remote_url = re.sub(r"\.git$", "", remote_url)
        repo = remote_url
        parts = repo.split("/")
        if len(parts) >= 1:
            org = parts[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        author = subprocess.check_output(
            ["git", "-C", project_dir, "config", "user.name"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return repo, org, author


def detect_environment():
    """Detect the execution environment."""
    if os.environ.get("CODESPACES"):
        return "codespace"
    if os.environ.get("REPL_ID"):
        return "replit"
    return "local"


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------


def find_session_files(sessions_dir=None, session_id=None):
    """Find JSONL session files.

    Returns a list of (session_id, file_path) tuples.
    """
    if sessions_dir is None:
        sessions_dir = os.path.expanduser("~/.claude/projects")

    results = []

    if session_id:
        # Search all project dirs for this specific session
        pattern = os.path.join(sessions_dir, "**", f"{session_id}.jsonl")
        for path in glob.glob(pattern, recursive=True):
            results.append((session_id, path))
        return results

    # Scan all project directories
    pattern = os.path.join(sessions_dir, "**", "*.jsonl")
    for path in glob.glob(pattern, recursive=True):
        basename = os.path.basename(path)
        if basename.endswith(".jsonl"):
            sid = basename[:-6]  # strip .jsonl
            results.append((sid, path))

    return results


# ---------------------------------------------------------------------------
# JSONL parsing
# ---------------------------------------------------------------------------


def parse_jsonl_file(filepath):
    """Parse a JSONL file, returning a list of records.

    Skips malformed lines with a warning to stderr.
    """
    records = []
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError as e:
                print(
                    f"WARNING: Malformed JSON at {filepath}:{line_num}: {e}",
                    file=sys.stderr,
                )
    return records


def build_linked_list(records):
    """Build ordered record list by following parentUuid -> uuid chain.

    Returns records in conversation order.
    """
    by_uuid = {}
    for r in records:
        uid = r.get("uuid")
        if uid:
            by_uuid[uid] = r

    # Find root: record whose parentUuid is absent or not in the dict
    roots = []
    for r in records:
        parent = r.get("parentUuid")
        if not parent or parent not in by_uuid:
            roots.append(r)

    if not roots:
        # Fallback: return in file order
        return records

    # Build children index: parentUuid -> list of children
    children = {}
    for r in records:
        parent = r.get("parentUuid")
        if parent:
            children.setdefault(parent, []).append(r)

    # Walk from roots in order using iterative DFS
    ordered = []
    visited = set()
    # Sort roots by timestamp to ensure deterministic ordering
    roots.sort(key=lambda r: r.get("timestamp", ""))

    stack = list(reversed(roots))
    while stack:
        node = stack.pop()
        uid = node.get("uuid")
        if uid and uid in visited:
            continue
        if uid:
            visited.add(uid)
        ordered.append(node)
        # Add children in reverse order so first child is processed first
        node_children = children.get(uid, [])
        node_children.sort(key=lambda r: r.get("timestamp", ""))
        for child in reversed(node_children):
            child_uid = child.get("uuid")
            if child_uid and child_uid not in visited:
                stack.append(child)

    # Add any records we did not visit (e.g. records without uuid)
    visited_uuids = visited
    for r in records:
        uid = r.get("uuid")
        if uid and uid not in visited_uuids:
            ordered.append(r)
        elif not uid:
            ordered.append(r)

    return ordered


# ---------------------------------------------------------------------------
# Tool result matching
# ---------------------------------------------------------------------------


def build_tool_result_map(ordered_records):
    """Build a map of tool_use_id -> tool_result info from user records.

    Scans user records for tool_result content blocks and toolUseResult
    top-level fields.  Returns {tool_use_id: {result_record, content_block,
    toolUseResult}}.
    """
    result_map = {}

    for record in ordered_records:
        if record.get("type") != "user":
            continue

        message = record.get("message", {})
        content = message.get("content")
        tool_use_result = record.get("toolUseResult")
        source_tool_use_id = record.get("sourceToolUseID")

        # Handle content array with tool_result blocks
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    tuid = block.get("tool_use_id")
                    if tuid:
                        result_map[tuid] = {
                            "record": record,
                            "content_block": block,
                            "toolUseResult": tool_use_result,
                        }

        # Also handle sourceToolUseID for direct matching
        if source_tool_use_id and source_tool_use_id not in result_map:
            result_map[source_tool_use_id] = {
                "record": record,
                "content_block": None,
                "toolUseResult": tool_use_result,
            }

    return result_map


# ---------------------------------------------------------------------------
# Extract target file from tool input/result
# ---------------------------------------------------------------------------


def extract_target_file(tool_name, input_obj, tool_use_result):
    """Extract the primary file path from a tool call."""
    if isinstance(input_obj, dict):
        for key in ("file_path", "filePath", "notebook_path", "path"):
            val = input_obj.get(key)
            if val and isinstance(val, str) and ("/" in val or "." in val):
                return val
        # Bash: try to extract from command
        if tool_name == "Bash":
            cmd = input_obj.get("command", "")
            # Look for file paths in common patterns
            m = re.search(r'(?:cat|less|head|tail|rm|cp|mv|touch|chmod)\s+["\']?([^\s"\'|;]+)', cmd)
            if m:
                return m.group(1)

    if isinstance(tool_use_result, dict):
        fp = tool_use_result.get("filePath")
        if fp:
            return fp

    return None


def extract_target_domain(tool_name, input_obj):
    """Extract target domain for web tools."""
    if tool_name != "WebFetch":
        return None
    if not isinstance(input_obj, dict):
        return None
    url = input_obj.get("url", "")
    m = re.match(r"https?://([^/]+)", url)
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Extract files referenced from text content
# ---------------------------------------------------------------------------


def extract_files_referenced(text):
    """Extract file paths mentioned in text content."""
    if not text:
        return []
    # Match common file path patterns
    paths = set()
    # Absolute paths
    for m in re.finditer(r"(/[\w./-]+\.[\w]+)", text):
        p = m.group(1)
        if len(p) > 5 and not p.startswith("//"):
            paths.add(p)
    # Relative paths with extension
    for m in re.finditer(r"(?:^|\s)([\w./-]+\.(?:py|ts|js|tsx|jsx|json|md|sql|sh|css|html|yml|yaml|toml|rs|go|java|rb|php|c|cpp|h))\b", text):
        p = m.group(1)
        if "/" in p:
            paths.add(p)
    return list(paths)[:20]  # Limit to 20


# ---------------------------------------------------------------------------
# Session parser
# ---------------------------------------------------------------------------


class SessionParser:
    """Parses a single session JSONL file into structured data."""

    def __init__(self, session_id, filepath, repo, org, author, environment):
        self.session_id = session_id
        self.filepath = filepath
        self.repo = repo
        self.org = org
        self.author = author
        self.environment = environment

        # Parsed outputs
        self.messages = []
        self.tool_calls = []
        self.session_meta = {}

        # Internal state
        self._message_index = 0
        self._call_index = 0
        self._models_used = set()
        self._agents_used = set()
        self._plugins_used = set()
        self._skills_used = set()
        self._git_branches = set()
        self._permission_modes = set()
        self._security_flags = set()
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_cache_read_tokens = 0
        self._total_cache_creation_tokens = 0
        self._total_thinking_chars = 0
        self._total_user_messages = 0
        self._total_assistant_messages = 0
        self._total_thinking_blocks = 0
        self._total_tool_results = 0
        self._total_system_events = 0
        self._total_failures = 0
        self._total_rejections = 0
        self._app_tool_calls = 0
        self._infra_tool_calls = 0
        self._compaction_count = 0
        self._has_continuation = False
        self._sensitive_files_touched = 0
        self._destructive_commands = 0
        self._first_message_at = None
        self._last_message_at = None
        self._claude_version = None
        self._primary_model = None
        self._session_date = None

    def parse(self):
        """Parse the session file and populate messages/tool_calls/session_meta."""
        raw_records = parse_jsonl_file(self.filepath)
        if not raw_records:
            return

        ordered = build_linked_list(raw_records)
        tool_result_map = build_tool_result_map(ordered)

        for record in ordered:
            rtype = record.get("type")

            # Skip sidechain records
            if record.get("isSidechain"):
                continue

            if rtype in SKIP_TYPES:
                continue

            if rtype not in PROCESS_TYPES:
                continue

            # Track timestamps
            ts = record.get("timestamp")
            if ts:
                if self._first_message_at is None or ts < self._first_message_at:
                    self._first_message_at = ts
                    # Derive session_date early so tool_calls get it during iteration
                    try:
                        dt = datetime.datetime.fromisoformat(
                            self._first_message_at.replace("Z", "+00:00")
                        )
                        self._session_date = dt.strftime("%Y-%m-%d")
                    except (ValueError, AttributeError):
                        pass
                if self._last_message_at is None or ts > self._last_message_at:
                    self._last_message_at = ts

            # Track metadata
            version = record.get("version")
            if version and not self._claude_version:
                self._claude_version = version

            branch = record.get("gitBranch")
            if branch:
                self._git_branches.add(branch)

            perm_mode = record.get("permissionMode")
            if perm_mode:
                self._permission_modes.add(perm_mode)

            # Detect continuation
            if record.get("isCompactSummary"):
                self._has_continuation = True

            if rtype == "user":
                self._process_user(record, tool_result_map)
            elif rtype == "assistant":
                self._process_assistant(record, tool_result_map)
            elif rtype == "system":
                self._process_system(record)

        # session_date was already derived during the loop (for tool_calls)
        # just ensure it's set if _first_message_at was found
        if self._first_message_at and not self._session_date:
            try:
                dt = datetime.datetime.fromisoformat(
                    self._first_message_at.replace("Z", "+00:00")
                )
                self._session_date = dt.strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                self._session_date = None

        # Build session metadata
        self.session_meta = self._build_session_meta()

    def _process_user(self, record, tool_result_map):
        """Process a user record."""
        message = record.get("message", {})
        content = message.get("content")
        ts = record.get("timestamp")
        branch = record.get("gitBranch")
        perm_mode = record.get("permissionMode")

        # Compaction summary
        if record.get("isCompactSummary"):
            self._compaction_count += 1
            text_content = ""
            if isinstance(content, str):
                text_content = content
            elif isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, str):
                        parts.append(block)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", ""))
                text_content = "\n".join(parts)

            self.messages.append({
                "session_id": self.session_id,
                "message_index": self._message_index,
                "role": "user",
                "message_type": "compaction_summary",
                "content": truncate(text_content),
                "thinking_length": None,
                "model": None,
                "input_tokens": None,
                "output_tokens": None,
                "cache_read_tokens": None,
                "cache_creation_tokens": None,
                "permission_mode": perm_mode,
                "git_branch": branch,
                "is_compaction_summary": True,
                "tool_use_id": None,
                "is_error": None,
                "files_referenced": extract_files_referenced(text_content),
                "skills_invoked": [],
                "tool_call_count": 0,
                "tool_failure_count": 0,
                "created_at": ts,
            })
            self._message_index += 1
            return

        # Check if content is a string (user typed text)
        if isinstance(content, str):
            self._total_user_messages += 1
            files_ref = extract_files_referenced(content)
            skills_inv = []
            # Detect skill invocations (e.g., "/commit", "/log")
            for m in re.finditer(r"(?:^|\s)/(\w[\w:-]*)", content):
                skills_inv.append(m.group(1))

            self.messages.append({
                "session_id": self.session_id,
                "message_index": self._message_index,
                "role": "user",
                "message_type": "text",
                "content": truncate(content),
                "thinking_length": None,
                "model": None,
                "input_tokens": None,
                "output_tokens": None,
                "cache_read_tokens": None,
                "cache_creation_tokens": None,
                "permission_mode": perm_mode,
                "git_branch": branch,
                "is_compaction_summary": False,
                "tool_use_id": None,
                "is_error": None,
                "files_referenced": files_ref,
                "skills_invoked": skills_inv,
                "tool_call_count": 0,
                "tool_failure_count": 0,
                "created_at": ts,
            })
            self._message_index += 1
            return

        # Content is an array -- may contain tool_result blocks or text
        if isinstance(content, list):
            has_text = False
            tool_results_in_msg = 0
            tool_failures_in_msg = 0

            for block in content:
                if isinstance(block, str):
                    # Inline text in a user message
                    if not has_text:
                        self._total_user_messages += 1
                        has_text = True
                        self.messages.append({
                            "session_id": self.session_id,
                            "message_index": self._message_index,
                            "role": "user",
                            "message_type": "text",
                            "content": truncate(block),
                            "thinking_length": None,
                            "model": None,
                            "input_tokens": None,
                            "output_tokens": None,
                            "cache_read_tokens": None,
                            "cache_creation_tokens": None,
                            "permission_mode": perm_mode,
                            "git_branch": branch,
                            "is_compaction_summary": False,
                            "tool_use_id": None,
                            "is_error": None,
                            "files_referenced": extract_files_referenced(block),
                            "skills_invoked": [],
                            "tool_call_count": 0,
                            "tool_failure_count": 0,
                            "created_at": ts,
                        })
                        self._message_index += 1
                    continue

                if not isinstance(block, dict):
                    continue

                block_type = block.get("type")

                if block_type == "tool_result":
                    self._total_tool_results += 1
                    tool_results_in_msg += 1
                    tuid = block.get("tool_use_id")
                    is_error = block.get("is_error", False)
                    if is_error:
                        tool_failures_in_msg += 1

                    # Extract content from tool_result block
                    result_content = block.get("content", "")
                    if isinstance(result_content, list):
                        text_parts = []
                        for rc in result_content:
                            if isinstance(rc, dict) and rc.get("type") == "text":
                                text_parts.append(rc.get("text", ""))
                            elif isinstance(rc, str):
                                text_parts.append(rc)
                        result_content = "\n".join(text_parts)
                    elif not isinstance(result_content, str):
                        result_content = str(result_content)

                    self.messages.append({
                        "session_id": self.session_id,
                        "message_index": self._message_index,
                        "role": "user",
                        "message_type": "tool_result",
                        "content": truncate(result_content),
                        "thinking_length": None,
                        "model": None,
                        "input_tokens": None,
                        "output_tokens": None,
                        "cache_read_tokens": None,
                        "cache_creation_tokens": None,
                        "permission_mode": perm_mode,
                        "git_branch": branch,
                        "is_compaction_summary": False,
                        "tool_use_id": tuid,
                        "is_error": is_error,
                        "files_referenced": extract_files_referenced(result_content),
                        "skills_invoked": [],
                        "tool_call_count": 0,
                        "tool_failure_count": 0,
                        "created_at": ts,
                    })
                    self._message_index += 1

                elif block_type == "text":
                    if not has_text:
                        self._total_user_messages += 1
                        has_text = True
                        text_val = block.get("text", "")
                        self.messages.append({
                            "session_id": self.session_id,
                            "message_index": self._message_index,
                            "role": "user",
                            "message_type": "text",
                            "content": truncate(text_val),
                            "thinking_length": None,
                            "model": None,
                            "input_tokens": None,
                            "output_tokens": None,
                            "cache_read_tokens": None,
                            "cache_creation_tokens": None,
                            "permission_mode": perm_mode,
                            "git_branch": branch,
                            "is_compaction_summary": False,
                            "tool_use_id": None,
                            "is_error": None,
                            "files_referenced": extract_files_referenced(text_val),
                            "skills_invoked": [],
                            "tool_call_count": 0,
                            "tool_failure_count": 0,
                            "created_at": ts,
                        })
                        self._message_index += 1

    def _process_assistant(self, record, tool_result_map):
        """Process an assistant record with content block splitting."""
        message = record.get("message", {})
        content_blocks = message.get("content", [])
        model = message.get("model")
        usage = message.get("usage", {})
        ts = record.get("timestamp")
        branch = record.get("gitBranch")
        perm_mode = record.get("permissionMode")

        if model:
            self._models_used.add(model)
            if not self._primary_model:
                self._primary_model = model

        # Token accounting (attribute all to first text/thinking block)
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        cache_read = usage.get("cache_read_input_tokens")
        cache_creation = usage.get("cache_creation_input_tokens")

        if input_tokens:
            self._total_input_tokens += input_tokens
        if output_tokens:
            self._total_output_tokens += output_tokens
        if cache_read:
            self._total_cache_read_tokens += cache_read
        if cache_creation:
            self._total_cache_creation_tokens += cache_creation

        tokens_attributed = False
        tool_call_count_for_msg = 0
        tool_failure_count_for_msg = 0
        first_text_idx = None

        if not isinstance(content_blocks, list):
            content_blocks = []

        for block in content_blocks:
            if not isinstance(block, dict):
                continue

            block_type = block.get("type")

            if block_type == "text":
                self._total_assistant_messages += 1
                text_val = block.get("text", "")
                files_ref = extract_files_referenced(text_val)

                msg = {
                    "session_id": self.session_id,
                    "message_index": self._message_index,
                    "role": "assistant",
                    "message_type": "text",
                    "content": truncate(text_val),
                    "thinking_length": None,
                    "model": model,
                    "input_tokens": input_tokens if not tokens_attributed else None,
                    "output_tokens": output_tokens if not tokens_attributed else None,
                    "cache_read_tokens": cache_read if not tokens_attributed else None,
                    "cache_creation_tokens": cache_creation if not tokens_attributed else None,
                    "permission_mode": perm_mode,
                    "git_branch": branch,
                    "is_compaction_summary": False,
                    "tool_use_id": None,
                    "is_error": record.get("isApiErrorMessage", False),
                    "files_referenced": files_ref,
                    "skills_invoked": [],
                    "tool_call_count": 0,  # Updated after counting tool_use blocks
                    "tool_failure_count": 0,
                    "created_at": ts,
                }
                tokens_attributed = True
                if first_text_idx is None:
                    first_text_idx = len(self.messages)
                self.messages.append(msg)
                self._message_index += 1

            elif block_type == "thinking":
                self._total_thinking_blocks += 1
                thinking_text = block.get("thinking", "")
                thinking_len = len(thinking_text) if thinking_text else 0
                self._total_thinking_chars += thinking_len

                msg = {
                    "session_id": self.session_id,
                    "message_index": self._message_index,
                    "role": "assistant",
                    "message_type": "thinking",
                    "content": truncate(thinking_text),
                    "thinking_length": thinking_len,
                    "model": model,
                    "input_tokens": input_tokens if not tokens_attributed else None,
                    "output_tokens": output_tokens if not tokens_attributed else None,
                    "cache_read_tokens": cache_read if not tokens_attributed else None,
                    "cache_creation_tokens": cache_creation if not tokens_attributed else None,
                    "permission_mode": perm_mode,
                    "git_branch": branch,
                    "is_compaction_summary": False,
                    "tool_use_id": None,
                    "is_error": False,
                    "files_referenced": [],
                    "skills_invoked": [],
                    "tool_call_count": 0,
                    "tool_failure_count": 0,
                    "created_at": ts,
                }
                tokens_attributed = True
                self.messages.append(msg)
                self._message_index += 1

            elif block_type == "tool_use":
                tool_call_count_for_msg += 1
                tool_call = self._process_tool_use(
                    block, record, tool_result_map, ts, branch
                )
                if tool_call and not tool_call.get("success", True):
                    tool_failure_count_for_msg += 1

        # Update the first text message with tool counts
        if first_text_idx is not None:
            self.messages[first_text_idx]["tool_call_count"] = tool_call_count_for_msg
            self.messages[first_text_idx]["tool_failure_count"] = tool_failure_count_for_msg

    def _process_tool_use(self, block, assistant_record, tool_result_map, ts, branch):
        """Process a tool_use content block into a tool_calls row."""
        tool_use_id = block.get("id")
        tool_name = block.get("name", "unknown")
        input_obj = block.get("input", {})
        caller = block.get("caller", {})
        caller_type = caller.get("type", "direct")

        category = classify_tool(tool_name)
        plugin_name = extract_plugin_name(tool_name)

        # Look up the matching tool result
        result_info = tool_result_map.get(tool_use_id, {})
        result_record = result_info.get("record")
        result_block = result_info.get("content_block")
        tool_use_result = result_info.get("toolUseResult")

        # Determine success/failure
        success = None
        was_rejected = False
        error_type = None
        error_message = None
        exit_code = None
        was_interrupted = False
        was_truncated_flag = False
        is_background = False
        background_task_id = None
        result_duration_ms = None

        # Check input for background flag
        if isinstance(input_obj, dict):
            is_background = bool(input_obj.get("run_in_background"))

        if result_block:
            is_error = result_block.get("is_error", False)
            success = not is_error
            if is_error:
                self._total_failures += 1
                error_type = "other"
                # Try to extract error message from result content
                rc = result_block.get("content", "")
                if isinstance(rc, list):
                    text_parts = []
                    for item in rc:
                        if isinstance(item, dict) and item.get("type") == "text":
                            text_parts.append(item.get("text", ""))
                        elif isinstance(item, str):
                            text_parts.append(item)
                    rc = "\n".join(text_parts)
                error_message = truncate(str(rc), SUMMARY_TRUNCATE)

        # Determine rejection from toolUseResult
        if isinstance(tool_use_result, str):
            lower_result = tool_use_result.lower()
            if "rejected" in lower_result or "denied" in lower_result:
                was_rejected = True
                success = False
                error_type = "rejected"
                error_message = truncate(tool_use_result, SUMMARY_TRUNCATE)
                self._total_rejections += 1
                self._total_failures += (1 if result_block and not result_block.get("is_error") else 0)

        # Extract information from toolUseResult dict
        if isinstance(tool_use_result, dict):
            if tool_use_result.get("interrupted"):
                was_interrupted = True
            if tool_use_result.get("truncated"):
                was_truncated_flag = True

            tur_exit = None
            # Bash exit code: look for returnCodeInterpretation or stderr presence
            if tool_name == "Bash":
                if "returnCodeInterpretation" in tool_use_result:
                    interp = tool_use_result["returnCodeInterpretation"]
                    if interp == "error":
                        if success is None:
                            success = False
                            error_type = "exit_code"
                            self._total_failures += 1

            bg_task_id = tool_use_result.get("backgroundTaskId")
            if bg_task_id:
                is_background = True
                background_task_id = bg_task_id

            dur = tool_use_result.get("durationMs")
            if dur is not None:
                result_duration_ms = dur

            if success is None:
                # If we have a result but no error indicator, assume success
                success = True

        elif isinstance(tool_use_result, list):
            # Array shape: multiple results -- assume success if present
            if success is None:
                success = True

        # If we still have no result at all, success stays None
        # (tool may have been interrupted or session ended)

        # Determine target file and domain
        target_file = extract_target_file(tool_name, input_obj, tool_use_result)
        target_domain = extract_target_domain(tool_name, input_obj)

        # Security checks
        sensitive = is_sensitive_file(target_file) if target_file else False
        if sensitive:
            self._sensitive_files_touched += 1

        secret_exposure = False
        output_text = summarize_output(tool_name, tool_use_result)
        if has_secret_exposure(output_text):
            secret_exposure = True

        destructive = False
        if tool_name == "Bash" and isinstance(input_obj, dict):
            cmd = input_obj.get("command", "")
            if is_destructive_command(cmd):
                destructive = True
                self._destructive_commands += 1

        security_flags = []
        if sensitive:
            security_flags.append("sensitive_file")
        if secret_exposure:
            security_flags.append("secret_exposure")
        if destructive:
            security_flags.append("destructive_command")
        if was_rejected:
            security_flags.append("user_rejection")

        # Session-level security flags
        for flag in security_flags:
            self._security_flags.add(flag)

        # Agent detection
        is_agent = (tool_name == "Task")
        agent_type = None
        agent_id = None
        agent_tokens = None
        agent_tool_count = None
        agent_duration_ms = None

        if is_agent:
            if isinstance(input_obj, dict):
                desc = input_obj.get("description", "")
                agent_type = truncate(desc, 100)
            if isinstance(tool_use_result, dict):
                agent_id = tool_use_result.get("agentId")
                agent_tokens = tool_use_result.get("totalTokens")
                agent_tool_count = tool_use_result.get("totalToolUseCount")
                agent_duration_ms = tool_use_result.get("totalDurationMs")
            self._agents_used.add(agent_type or "unknown")

        # Plugin tracking
        if plugin_name:
            self._plugins_used.add(plugin_name)

        # Skill tracking
        if tool_name == "Skill" and isinstance(input_obj, dict):
            skill_name = input_obj.get("skill", "")
            if skill_name:
                self._skills_used.add(skill_name)

        # Skill tracking from toolUseResult
        if isinstance(tool_use_result, dict):
            command_name = tool_use_result.get("commandName")
            if command_name:
                self._skills_used.add(command_name)

        # Infra vs app tool call classification
        if tool_name == "Bash" and isinstance(input_obj, dict):
            cmd = input_obj.get("command", "")
            if is_infra_command(cmd):
                self._infra_tool_calls += 1
            else:
                self._app_tool_calls += 1
        else:
            self._app_tool_calls += 1

        # Estimate duration from timestamps
        duration_ms = None
        if result_record and ts:
            result_ts = result_record.get("timestamp")
            if result_ts:
                try:
                    t1 = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    t2 = datetime.datetime.fromisoformat(result_ts.replace("Z", "+00:00"))
                    delta = (t2 - t1).total_seconds() * 1000
                    if delta >= 0:
                        duration_ms = int(delta)
                except (ValueError, TypeError):
                    pass

        # Was blocked by hook?
        was_blocked_by_hook = False
        if result_record:
            # Look for hook blocking indicators
            if isinstance(tool_use_result, dict):
                if tool_use_result.get("status") == "blocked_by_hook":
                    was_blocked_by_hook = True

        input_summary = summarize_input(tool_name, input_obj)

        tool_call = {
            "session_id": self.session_id,
            "message_id": None,  # Will be set after insert
            "call_index": self._call_index,
            "tool_name": tool_name,
            "tool_category": category,
            "input_summary": input_summary,
            "output_summary": output_text,
            "success": success,
            "was_rejected": was_rejected,
            "error_type": error_type,
            "error_message": error_message,
            "exit_code": exit_code,
            "target_file": target_file,
            "target_domain": target_domain,
            "is_background": is_background,
            "is_agent": is_agent,
            "agent_type": agent_type,
            "plugin_name": plugin_name,
            "is_sensitive_file": sensitive,
            "has_secret_exposure": secret_exposure,
            "is_destructive": destructive,
            "was_blocked_by_hook": was_blocked_by_hook,
            "security_flags": security_flags,
            "caller_type": caller_type,
            "was_interrupted": was_interrupted,
            "was_truncated": was_truncated_flag,
            "agent_id": agent_id,
            "agent_tokens": agent_tokens,
            "agent_tool_count": agent_tool_count,
            "agent_duration_ms": agent_duration_ms,
            "background_task_id": background_task_id,
            "result_duration_ms": result_duration_ms,
            "duration_ms": duration_ms,
            "repo": self.repo,
            "org": self.org,
            "session_date": self._session_date,
            "created_at": ts,
        }

        self.tool_calls.append(tool_call)
        self._call_index += 1
        return tool_call

    def _process_system(self, record):
        """Process a system record."""
        self._total_system_events += 1
        content = record.get("content", "")
        ts = record.get("timestamp")
        subtype = record.get("subtype", "")

        # Detect compaction
        is_compaction = False
        if record.get("compactMetadata"):
            is_compaction = True
            self._compaction_count += 1

        message_type = "compaction_summary" if is_compaction else "system"

        self.messages.append({
            "session_id": self.session_id,
            "message_index": self._message_index,
            "role": "system",
            "message_type": message_type,
            "content": truncate(str(content) if content else ""),
            "thinking_length": None,
            "model": None,
            "input_tokens": None,
            "output_tokens": None,
            "cache_read_tokens": None,
            "cache_creation_tokens": None,
            "permission_mode": None,
            "git_branch": None,
            "is_compaction_summary": is_compaction,
            "tool_use_id": None,
            "is_error": None,
            "files_referenced": [],
            "skills_invoked": [],
            "tool_call_count": 0,
            "tool_failure_count": 0,
            "created_at": ts,
        })
        self._message_index += 1

    def _build_session_meta(self):
        """Build the session-level aggregate row."""
        return {
            "session_id": self.session_id,
            "repo": self.repo,
            "org": self.org,
            "author": self.author,
            "app_name": self.repo.split("/")[-1] if self.repo else None,
            "environment": self.environment,
            "claude_version": self._claude_version,
            "model": self._primary_model,
            "session_date": self._session_date,
            "first_message_at": self._first_message_at,
            "last_message_at": self._last_message_at,
            "total_messages": len(self.messages),
            "total_user_messages": self._total_user_messages,
            "total_assistant_messages": self._total_assistant_messages,
            "total_thinking_blocks": self._total_thinking_blocks,
            "total_tool_results": self._total_tool_results,
            "total_system_events": self._total_system_events,
            "total_tool_calls": len(self.tool_calls),
            "total_failures": self._total_failures,
            "total_rejections": self._total_rejections,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_cache_read_tokens": self._total_cache_read_tokens,
            "total_cache_creation_tokens": self._total_cache_creation_tokens,
            "total_thinking_chars": self._total_thinking_chars,
            "app_tool_calls": self._app_tool_calls,
            "infra_tool_calls": self._infra_tool_calls,
            "compaction_count": self._compaction_count,
            "has_continuation": self._has_continuation,
            "agents_used": sorted(self._agents_used),
            "plugins_used": sorted(self._plugins_used),
            "skills_used": sorted(self._skills_used),
            "git_branches": sorted(self._git_branches),
            "permission_modes": sorted(self._permission_modes),
            "models_used": sorted(self._models_used),
            "security_flags": sorted(self._security_flags),
            "sensitive_files_touched": self._sensitive_files_touched,
            "destructive_commands": self._destructive_commands,
            "ingested": True,
            "ingested_at": "now()",
        }

    def is_empty(self):
        """Check if the session has no messages and no tool calls."""
        return len(self.messages) == 0 and len(self.tool_calls) == 0


# ---------------------------------------------------------------------------
# SQL generation
# ---------------------------------------------------------------------------


def generate_session_insert(meta):
    """Generate an INSERT statement for the sessions table."""
    cols = [
        "session_id", "repo", "org", "author", "app_name", "environment",
        "claude_version", "model", "session_date", "first_message_at",
        "last_message_at", "total_messages", "total_user_messages",
        "total_assistant_messages", "total_thinking_blocks", "total_tool_results",
        "total_system_events", "total_tool_calls", "total_failures",
        "total_rejections", "total_input_tokens", "total_output_tokens",
        "total_cache_read_tokens", "total_cache_creation_tokens",
        "total_thinking_chars", "app_tool_calls", "infra_tool_calls",
        "compaction_count", "has_continuation", "agents_used", "plugins_used",
        "skills_used", "git_branches", "permission_modes", "models_used",
        "security_flags", "sensitive_files_touched", "destructive_commands",
        "ingested", "ingested_at",
    ]

    values = []
    for col in cols:
        val = meta.get(col)
        if col == "ingested_at":
            values.append("now()")
        elif col == "session_date" and val:
            values.append(f"'{val}'::date")
        elif col in ("first_message_at", "last_message_at") and val:
            values.append(f"{dollar_quote(val)}::timestamptz")
        elif col in (
            "agents_used", "plugins_used", "skills_used", "git_branches",
            "permission_modes", "models_used", "security_flags",
        ):
            values.append(sql_array_or_empty(val if val else []))
        elif col == "ingested":
            values.append("true")
        else:
            values.append(sql_value(val))

    col_str = ", ".join(cols)
    val_str = ", ".join(values)
    return (
        f"INSERT INTO sessions ({col_str})\n"
        f"VALUES ({val_str})\n"
        f"ON CONFLICT (session_id) DO UPDATE SET\n"
        f"  total_messages = EXCLUDED.total_messages,\n"
        f"  total_user_messages = EXCLUDED.total_user_messages,\n"
        f"  total_assistant_messages = EXCLUDED.total_assistant_messages,\n"
        f"  total_thinking_blocks = EXCLUDED.total_thinking_blocks,\n"
        f"  total_tool_results = EXCLUDED.total_tool_results,\n"
        f"  total_system_events = EXCLUDED.total_system_events,\n"
        f"  total_tool_calls = EXCLUDED.total_tool_calls,\n"
        f"  total_failures = EXCLUDED.total_failures,\n"
        f"  total_rejections = EXCLUDED.total_rejections,\n"
        f"  total_input_tokens = EXCLUDED.total_input_tokens,\n"
        f"  total_output_tokens = EXCLUDED.total_output_tokens,\n"
        f"  total_cache_read_tokens = EXCLUDED.total_cache_read_tokens,\n"
        f"  total_cache_creation_tokens = EXCLUDED.total_cache_creation_tokens,\n"
        f"  total_thinking_chars = EXCLUDED.total_thinking_chars,\n"
        f"  app_tool_calls = EXCLUDED.app_tool_calls,\n"
        f"  infra_tool_calls = EXCLUDED.infra_tool_calls,\n"
        f"  compaction_count = EXCLUDED.compaction_count,\n"
        f"  has_continuation = EXCLUDED.has_continuation,\n"
        f"  agents_used = EXCLUDED.agents_used,\n"
        f"  plugins_used = EXCLUDED.plugins_used,\n"
        f"  skills_used = EXCLUDED.skills_used,\n"
        f"  git_branches = EXCLUDED.git_branches,\n"
        f"  permission_modes = EXCLUDED.permission_modes,\n"
        f"  models_used = EXCLUDED.models_used,\n"
        f"  security_flags = EXCLUDED.security_flags,\n"
        f"  sensitive_files_touched = EXCLUDED.sensitive_files_touched,\n"
        f"  destructive_commands = EXCLUDED.destructive_commands,\n"
        f"  last_message_at = EXCLUDED.last_message_at,\n"
        f"  ingested = true,\n"
        f"  ingested_at = now();"
    )


def generate_session_update(meta):
    """Generate an UPDATE statement for the sessions table (incremental)."""
    sets = []
    for col in [
        "total_messages", "total_user_messages", "total_assistant_messages",
        "total_thinking_blocks", "total_tool_results", "total_system_events",
        "total_tool_calls", "total_failures", "total_rejections",
        "total_input_tokens", "total_output_tokens", "total_cache_read_tokens",
        "total_cache_creation_tokens", "total_thinking_chars",
        "app_tool_calls", "infra_tool_calls", "compaction_count",
        "sensitive_files_touched", "destructive_commands",
    ]:
        sets.append(f"  {col} = {sql_value(meta.get(col))}")

    for col in [
        "has_continuation",
    ]:
        sets.append(f"  {col} = {sql_value(meta.get(col))}")

    if meta.get("last_message_at"):
        sets.append(f"  last_message_at = {dollar_quote(meta['last_message_at'])}::timestamptz")

    for col in [
        "agents_used", "plugins_used", "skills_used", "git_branches",
        "permission_modes", "models_used", "security_flags",
    ]:
        val = meta.get(col, [])
        sets.append(f"  {col} = {sql_array_or_empty(val)}")

    sets.append("  ingested_at = now()")
    set_str = ",\n".join(sets)
    sid = dollar_quote(meta["session_id"])
    return f"UPDATE sessions SET\n{set_str}\nWHERE session_id = {sid};"


def generate_message_insert(msg):
    """Generate an INSERT statement for the messages table."""
    cols = [
        "session_id", "message_index", "role", "message_type", "content",
        "thinking_length", "model", "input_tokens", "output_tokens",
        "cache_read_tokens", "cache_creation_tokens", "permission_mode",
        "git_branch", "is_compaction_summary", "tool_use_id", "is_error",
        "files_referenced", "skills_invoked", "tool_call_count",
        "tool_failure_count", "created_at",
    ]

    values = []
    for col in cols:
        val = msg.get(col)
        if col == "created_at" and val:
            values.append(f"{dollar_quote(val)}::timestamptz")
        elif col in ("files_referenced", "skills_invoked"):
            values.append(sql_array_or_empty(val if val else []))
        else:
            values.append(sql_value(val))

    col_str = ", ".join(cols)
    val_str = ", ".join(values)
    return (
        f"INSERT INTO messages ({col_str})\n"
        f"VALUES ({val_str})\n"
        f"ON CONFLICT (session_id, message_index) DO NOTHING;"
    )


def generate_tool_call_insert(tc):
    """Generate an INSERT statement for the tool_calls table."""
    cols = [
        "session_id", "message_id", "call_index", "tool_name", "tool_category",
        "input_summary", "output_summary", "success", "was_rejected",
        "error_type", "error_message", "exit_code", "target_file",
        "target_domain", "is_background", "is_agent", "agent_type",
        "plugin_name", "is_sensitive_file", "has_secret_exposure",
        "is_destructive", "was_blocked_by_hook", "security_flags",
        "caller_type", "was_interrupted", "was_truncated", "agent_id",
        "agent_tokens", "agent_tool_count", "agent_duration_ms",
        "background_task_id", "result_duration_ms", "duration_ms",
        "repo", "org", "session_date", "created_at",
    ]

    values = []
    for col in cols:
        val = tc.get(col)
        if col == "created_at" and val:
            values.append(f"{dollar_quote(val)}::timestamptz")
        elif col == "session_date" and val:
            values.append(f"'{val}'::date")
        elif col == "security_flags":
            values.append(sql_array_or_empty(val if val else []))
        else:
            values.append(sql_value(val))

    col_str = ", ".join(cols)
    val_str = ", ".join(values)
    return (
        f"INSERT INTO tool_calls ({col_str})\n"
        f"VALUES ({val_str});"
    )


# ---------------------------------------------------------------------------
# Incremental logic
# ---------------------------------------------------------------------------


def should_skip_session(session_id, meta, incremental_state):
    """Determine if session should be skipped (already fully ingested).

    Returns: (skip, is_update, max_message_index, max_call_index)
    """
    if not incremental_state:
        return False, False, -1, -1

    existing = incremental_state.get(session_id)
    if not existing:
        # New session
        return False, False, -1, -1

    existing_last_message = existing.get("last_message_at")
    existing_total_messages = existing.get("total_messages", 0)
    existing_total_tool_calls = existing.get("total_tool_calls", 0)

    local_last_message = meta.get("last_message_at")
    local_total_messages = meta.get("total_messages", 0)
    local_total_tool_calls = meta.get("total_tool_calls", 0)

    # Exact match: skip entirely
    if (
        existing_total_messages == local_total_messages
        and existing_total_tool_calls == local_total_tool_calls
        and existing_last_message == local_last_message
    ):
        return True, False, -1, -1

    # Partial match: delta insert
    max_msg_idx = existing_total_messages - 1  # 0-indexed
    max_call_idx = existing_total_tool_calls - 1
    return False, True, max_msg_idx, max_call_idx


# ---------------------------------------------------------------------------
# Batch writing
# ---------------------------------------------------------------------------


def write_batches(statements, output_dir):
    """Write SQL statements to batch files.

    Returns the number of files written.
    """
    os.makedirs(output_dir, exist_ok=True)

    file_count = 0
    for i in range(0, len(statements), BATCH_SIZE):
        batch = statements[i : i + BATCH_SIZE]
        file_count += 1
        filename = f"batch_{file_count:03d}.sql"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            for stmt in batch:
                f.write(stmt)
                f.write("\n\n")

    return file_count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Session Hoardinator -- parse Claude Code JSONL session transcripts"
    )
    parser.add_argument(
        "--session",
        metavar="SESSION_ID",
        help="Parse a single session by ID",
    )
    parser.add_argument(
        "--project-dir",
        metavar="PATH",
        default=os.getcwd(),
        help="Project directory for namespace derivation (default: cwd)",
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        default="/tmp/hoardinator-sql/",
        help="Output directory for SQL batch files (default: /tmp/hoardinator-sql/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count only, do not write SQL files",
    )
    parser.add_argument(
        "--sessions-dir",
        metavar="PATH",
        help="Override ~/.claude/projects/ scan path",
    )
    parser.add_argument(
        "--incremental",
        metavar="JSON",
        help="JSON string with existing session states for delta detection",
    )
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Only process sessions from this date (based on file modification time)",
    )

    args = parser.parse_args()

    # Parse incremental state
    incremental_state = None
    if args.incremental:
        try:
            incremental_state = json.loads(args.incremental)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid --incremental JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Validate --date format
    date_filter = None
    if args.date:
        try:
            date_filter = datetime.date.fromisoformat(args.date)
        except ValueError:
            print(f"ERROR: Invalid --date format: {args.date} (expected YYYY-MM-DD)", file=sys.stderr)
            sys.exit(1)

    # Derive namespace
    repo, org, author = derive_namespace(args.project_dir)
    environment = detect_environment()

    # Find session files
    session_files = find_session_files(
        sessions_dir=args.sessions_dir,
        session_id=args.session,
    )

    if not session_files:
        print("No session files found.", file=sys.stderr)
        summary = {
            "new_sessions": 0,
            "updated_sessions": 0,
            "skipped_sessions": 0,
            "total_messages": 0,
            "total_tool_calls": 0,
        }
        if not args.dry_run:
            os.makedirs(args.output, exist_ok=True)
            summary_path = os.path.join(args.output, "summary.json")
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
        print(json.dumps(summary, indent=2))
        sys.exit(0)

    # Process sessions
    all_statements = []
    summary = {
        "new_sessions": 0,
        "updated_sessions": 0,
        "skipped_sessions": 0,
        "total_messages": 0,
        "total_tool_calls": 0,
    }

    for session_id, filepath in session_files:
        # Date filter: skip files not modified on the target date
        if date_filter:
            try:
                mtime = os.path.getmtime(filepath)
                file_date = datetime.date.fromtimestamp(mtime)
                if file_date != date_filter:
                    continue
            except OSError:
                continue

        print(f"Parsing session {session_id}...", file=sys.stderr)

        sp = SessionParser(session_id, filepath, repo, org, author, environment)
        try:
            sp.parse()
        except Exception as e:
            print(
                f"ERROR: Failed to parse session {session_id}: {e}",
                file=sys.stderr,
            )
            continue

        # Skip empty sessions
        if sp.is_empty():
            print(f"  Skipping empty session {session_id}", file=sys.stderr)
            summary["skipped_sessions"] += 1
            continue

        meta = sp.session_meta

        # Incremental detection
        skip, is_update, max_msg_idx, max_call_idx = should_skip_session(
            session_id, meta, incremental_state
        )

        if skip:
            print(f"  Skipping current session {session_id} (no changes)", file=sys.stderr)
            summary["skipped_sessions"] += 1
            continue

        if is_update:
            print(
                f"  Updating session {session_id} (delta from msg:{max_msg_idx} call:{max_call_idx})",
                file=sys.stderr,
            )
            summary["updated_sessions"] += 1

            # Session UPDATE instead of INSERT
            all_statements.append(generate_session_update(meta))

            # Only new messages
            for msg in sp.messages:
                if msg["message_index"] > max_msg_idx:
                    all_statements.append(generate_message_insert(msg))
                    summary["total_messages"] += 1

            # Only new tool calls
            for tc in sp.tool_calls:
                if tc["call_index"] > max_call_idx:
                    all_statements.append(generate_tool_call_insert(tc))
                    summary["total_tool_calls"] += 1
        else:
            print(f"  New session {session_id}", file=sys.stderr)
            summary["new_sessions"] += 1

            # Full INSERT
            all_statements.append(generate_session_insert(meta))

            for msg in sp.messages:
                all_statements.append(generate_message_insert(msg))
                summary["total_messages"] += 1

            for tc in sp.tool_calls:
                all_statements.append(generate_tool_call_insert(tc))
                summary["total_tool_calls"] += 1

    # Output
    if args.dry_run:
        print("\n--- DRY RUN ---", file=sys.stderr)
        print(f"New sessions:     {summary['new_sessions']}", file=sys.stderr)
        print(f"Updated sessions: {summary['updated_sessions']}", file=sys.stderr)
        print(f"Skipped sessions: {summary['skipped_sessions']}", file=sys.stderr)
        print(f"Total messages:   {summary['total_messages']}", file=sys.stderr)
        print(f"Total tool calls: {summary['total_tool_calls']}", file=sys.stderr)
        print(f"SQL statements:   {len(all_statements)}", file=sys.stderr)
    else:
        if all_statements:
            file_count = write_batches(all_statements, args.output)
            print(f"Wrote {file_count} batch file(s) to {args.output}", file=sys.stderr)
        else:
            os.makedirs(args.output, exist_ok=True)
            print("No SQL statements to write.", file=sys.stderr)

        # Write summary
        summary_path = os.path.join(args.output, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    # Print summary to stdout for callers to capture
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
