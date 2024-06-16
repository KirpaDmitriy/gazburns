CREATE DATABASE mydb;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
ALTER ROLE myuser SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
SHOW port;
