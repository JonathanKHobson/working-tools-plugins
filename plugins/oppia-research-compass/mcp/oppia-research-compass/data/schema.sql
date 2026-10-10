CREATE TABLE corpus_meta (
          root TEXT NOT NULL,
          built_at TEXT NOT NULL,
          source_files INTEGER NOT NULL,
          records INTEGER NOT NULL,
          exported_docs INTEGER NOT NULL,
          metadata_records INTEGER NOT NULL,
          runs INTEGER NOT NULL,
          words INTEGER NOT NULL,
          chars INTEGER NOT NULL,
          interview_records INTEGER NOT NULL,
          chunks INTEGER NOT NULL,
          qa_chunks INTEGER NOT NULL,
          section_chunks INTEGER NOT NULL
        );

CREATE TABLE records (
          record_id TEXT PRIMARY KEY,
          kind TEXT NOT NULL,
          title TEXT NOT NULL,
          sheet TEXT,
          row_number INTEGER,
          doc_id TEXT,
          run_id TEXT NOT NULL,
          source_count INTEGER NOT NULL,
          primary_source_path TEXT NOT NULL,
          primary_source_rel_path TEXT NOT NULL,
          primary_source_mtime REAL NOT NULL,
          primary_source_size_bytes INTEGER NOT NULL,
          content_sha256 TEXT NOT NULL,
          preview TEXT NOT NULL,
          headings_json TEXT NOT NULL,
          line_count INTEGER NOT NULL,
          word_count INTEGER NOT NULL,
          char_count INTEGER NOT NULL,
          source_paths_json TEXT NOT NULL,
          is_interview INTEGER NOT NULL,
          persona_json TEXT NOT NULL,
          persona_summary TEXT NOT NULL,
          section_count INTEGER NOT NULL,
          qa_count INTEGER NOT NULL,
          chunk_count INTEGER NOT NULL,
          chunk_types_json TEXT NOT NULL
        );

CREATE TABLE sources (
          source_id INTEGER PRIMARY KEY AUTOINCREMENT,
          record_id TEXT NOT NULL,
          source_path TEXT NOT NULL UNIQUE,
          source_rel_path TEXT NOT NULL,
          run_id TEXT NOT NULL,
          kind TEXT NOT NULL,
          sheet TEXT,
          row_number INTEGER,
          doc_id TEXT,
          title TEXT NOT NULL,
          mtime REAL NOT NULL,
          size_bytes INTEGER NOT NULL,
          content_sha256 TEXT NOT NULL,
          is_primary INTEGER NOT NULL,
          FOREIGN KEY (record_id) REFERENCES records (record_id) ON DELETE CASCADE
        );

CREATE TABLE evidence (
          evidence_id TEXT PRIMARY KEY,
          record_id TEXT NOT NULL,
          source_path TEXT NOT NULL,
          chunk_type TEXT NOT NULL,
          chunk_title TEXT NOT NULL,
          section_title TEXT,
          question_text TEXT,
          respondent_label TEXT,
          chunk_index INTEGER NOT NULL,
          content TEXT NOT NULL,
          content_sha256 TEXT NOT NULL,
          content_chars INTEGER NOT NULL,
          FOREIGN KEY (record_id) REFERENCES records (record_id) ON DELETE CASCADE
        );

CREATE TABLE release_meta (
          product TEXT NOT NULL,
          version TEXT NOT NULL,
          sanitized_at TEXT NOT NULL,
          source_snapshot_sha256 TEXT NOT NULL,
          distribution TEXT NOT NULL,
          email_addresses_redacted INTEGER NOT NULL
        );

CREATE INDEX idx_records_kind_sheet_row ON records (kind, sheet, row_number);

CREATE INDEX idx_records_interview ON records (is_interview, sheet, row_number);

CREATE INDEX idx_records_title ON records (title COLLATE NOCASE);

CREATE INDEX idx_sources_record ON sources (record_id, is_primary DESC, mtime DESC);

CREATE INDEX idx_sources_run ON sources (run_id);

CREATE INDEX idx_evidence_record ON evidence (record_id);

CREATE INDEX idx_evidence_chunk_type ON evidence (chunk_type, section_title, chunk_index);

CREATE VIRTUAL TABLE evidence_fts USING fts5(
          evidence_id UNINDEXED,
          record_id UNINDEXED,
          content,
          tokenize = 'unicode61'
        );
