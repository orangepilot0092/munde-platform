-- Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS pgvector;

-- Create a schema for geospatial data
CREATE SCHEMA IF NOT EXISTS gis;
GRANT ALL ON SCHEMA gis TO PUBLIC;
