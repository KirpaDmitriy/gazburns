CREATE TABLE "user" (
       id SERIAL PRIMARY KEY,
       username VARCHAR(100) UNIQUE,
       hashed_password VARCHAR(100)
);

INSERT INTO "user" (username, hashed_password) VALUES ('john_doe', '$2b$12$k6PEkL2pEY5wIw1SRHP6IuAECTFrjMAs1dx4aG9Xs2IvcsCk4HQXi');
