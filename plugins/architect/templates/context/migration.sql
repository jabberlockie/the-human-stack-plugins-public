-- Architect Context System - Database Migration
-- Run this SQL to set up pgvector for session context retrieval
--
-- Prerequisites:
--   - PostgreSQL 14+ with pgvector extension available
--   - Run as database owner or superuser

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create session embeddings table
CREATE TABLE IF NOT EXISTS session_embeddings (
  id SERIAL PRIMARY KEY,

  -- Content
  session_name TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,

  -- Vector embedding (OpenAI text-embedding-3-small = 1536 dimensions)
  embedding_vec vector(1536),

  -- Layer classification
  layer TEXT NOT NULL,        -- user, product, project, plan, task
  sublayer TEXT NOT NULL,     -- varies by layer (see below)

  -- Context identifiers
  project_name TEXT,
  feature_name TEXT,
  product_area TEXT,

  -- Classification metadata
  summary TEXT,
  topics TEXT[],

  -- Temporal
  session_date DATE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- Relationships
  tech_stack TEXT[],
  files_touched TEXT[],
  commit_hashes TEXT[],

  -- Ingestion metadata
  ingest_trigger TEXT,  -- precompact, plan_approved, commit, manual

  -- Constraints
  CONSTRAINT valid_layer CHECK (layer IN ('user', 'product', 'project', 'plan', 'task')),
  CONSTRAINT valid_sublayer CHECK (
    (layer = 'user' AND sublayer IN ('patterns', 'preferences', 'learnings', 'mistakes')) OR
    (layer = 'product' AND sublayer IN ('architecture', 'design', 'domain')) OR
    (layer = 'project' AND sublayer IN ('active', 'decisions', 'state')) OR
    (layer = 'plan' AND sublayer IN ('strategy', 'steps', 'backlog')) OR
    (layer = 'task' AND sublayer IN ('implementation', 'debugging', 'verification'))
  )
);

-- 3. Create indexes for efficient querying

-- Vector similarity search (IVFFlat for approximate nearest neighbor)
-- Note: For better accuracy on small datasets, use HNSW instead:
--   CREATE INDEX embedding_hnsw_idx ON session_embeddings
--     USING hnsw (embedding_vec vector_cosine_ops);
CREATE INDEX IF NOT EXISTS embedding_ivfflat_idx
  ON session_embeddings USING ivfflat (embedding_vec vector_cosine_ops)
  WITH (lists = 100);

-- Layer/sublayer filtering
CREATE INDEX IF NOT EXISTS layer_idx ON session_embeddings (layer);
CREATE INDEX IF NOT EXISTS sublayer_idx ON session_embeddings (sublayer);

-- Project filtering
CREATE INDEX IF NOT EXISTS project_idx ON session_embeddings (project_name);
CREATE INDEX IF NOT EXISTS product_area_idx ON session_embeddings (product_area);

-- Temporal queries
CREATE INDEX IF NOT EXISTS session_date_idx ON session_embeddings (session_date DESC);

-- Composite index for common query pattern
CREATE INDEX IF NOT EXISTS layer_project_idx ON session_embeddings (layer, project_name);

-- 4. Add comments for documentation
COMMENT ON TABLE session_embeddings IS 'Stores chunked and classified session transcripts for semantic retrieval';
COMMENT ON COLUMN session_embeddings.layer IS 'Context layer: user, product, project, plan, task';
COMMENT ON COLUMN session_embeddings.sublayer IS 'Sublayer within the layer (e.g., user/patterns, product/architecture)';
COMMENT ON COLUMN session_embeddings.embedding_vec IS 'OpenAI text-embedding-3-small vector (1536 dimensions)';
COMMENT ON COLUMN session_embeddings.ingest_trigger IS 'What triggered ingestion: precompact, plan_approved, commit, manual';

-- 5. Grant permissions (adjust role name as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON session_embeddings TO your_app_role;
-- GRANT USAGE, SELECT ON session_embeddings_id_seq TO your_app_role;
