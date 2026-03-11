CREATE TABLE skills (
    skill_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    module_path TEXT NOT NULL,
    entry_function TEXT NOT NULL,
    version TEXT DEFAULT '1.0.0',
    description TEXT,
    dependencies TEXT,        -- JSON array
    health_status TEXT DEFAULT 'unknown',
    last_invoked TIMESTAMP,
    invocation_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skill_endpoints (
    endpoint_id TEXT PRIMARY KEY,
    skill_id TEXT REFERENCES skills(skill_id),
    route TEXT NOT NULL,
    method TEXT DEFAULT 'POST',
    description TEXT
);
