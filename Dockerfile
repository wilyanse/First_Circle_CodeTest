# Use the official PostgreSQL image
FROM postgres:latest

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/