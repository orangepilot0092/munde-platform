-- Enable PostGIS for geospatial support
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable pgvector for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create initial schema if needed
CREATE SCHEMA IF NOT EXISTS sahyadri;
