CREATE TABLE "case" (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    images JSON,
    meta_information JSON
);

CREATE INDEX idx_case_id ON "case" (id);
CREATE INDEX idx_case_username ON "case" (username);
