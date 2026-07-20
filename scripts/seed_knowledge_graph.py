import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)
engine = create_engine(settings.DATABASE_URL)

setup_sql = """
-- Safely drop and recreate to ensure exact schema match for Sprint 24
DROP TABLE IF EXISTS graph_relationships CASCADE;
DROP TABLE IF EXISTS graph_entities CASCADE;

CREATE TABLE graph_entities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(100) NOT NULL,
    metadata JSONB
);

CREATE TABLE graph_relationships (
    id SERIAL PRIMARY KEY,
    source_id INT REFERENCES graph_entities(id) ON DELETE CASCADE,
    target_id INT REFERENCES graph_entities(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL,
    UNIQUE(source_id, target_id, relationship_type)
);
"""

seed_sql = """
-- 1. Insert State and Districts
INSERT INTO graph_entities (name, type, metadata) VALUES
('Maharashtra', 'State', '{"code": "MH"}'),
('Pune', 'District', NULL), ('Mumbai', 'District', NULL), ('Nashik', 'District', NULL),
('Kolhapur', 'District', NULL), ('Solapur', 'District', NULL), ('Aurangabad', 'District', NULL),
('Nagpur', 'District', NULL), ('Thane', 'District', NULL), ('Satara', 'District', NULL),
('Sangli', 'District', NULL), ('Ahmednagar', 'District', NULL), ('Jalgaon', 'District', NULL),
('Ratnagiri', 'District', NULL), ('Sindhudurg', 'District', NULL), ('Raigad', 'District', NULL),
('Palghar', 'District', NULL), ('Dhule', 'District', NULL), ('Nandurbar', 'District', NULL),
('Jalna', 'District', NULL), ('Parbhani', 'District', NULL), ('Hingoli', 'District', NULL),
('Nanded', 'District', NULL), ('Beed', 'District', NULL), ('Latur', 'District', NULL),
('Osmanabad', 'District', NULL), ('Amravati', 'District', NULL), ('Akola', 'District', NULL),
('Buldhana', 'District', NULL), ('Washim', 'District', NULL), ('Yavatmal', 'District', NULL),
('Wardha', 'District', NULL), ('Bhandara', 'District', NULL), ('Gondia', 'District', NULL),
('Chandrapur', 'District', NULL), ('Gadchiroli', 'District', NULL),
-- 2. Insert Rivers, Reservoirs, Crops
('Godavari', 'River', '{"length_km": 1465, "origin": "Trimbakeshwar"}'),
('Krishna', 'River', '{"length_km": 1400, "origin": "Mahabaleshwar"}'),
('Bhima', 'River', '{"length_km": 861, "origin": "Bhimashankar"}'),
('Ujani', 'Reservoir', '{"capacity_tmc": 118, "river": "Bhima"}'),
('Koyna', 'Reservoir', '{"capacity_tmc": 105, "river": "Koyna"}'),
('Sugarcane', 'Crop', '{"season": "Kharif/Rabi", "water_intensive": true}'),
('Cotton', 'Crop', '{"season": "Kharif", "water_intensive": false}'),
('Soybean', 'Crop', '{"season": "Kharif", "water_intensive": false}');

-- 3. Insert Relationships
INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Bhima'),
    (SELECT id FROM graph_entities WHERE name = 'Pune'),
    'flows_through'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Bhima') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Pune') AND relationship_type = 'flows_through');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Godavari'),
    (SELECT id FROM graph_entities WHERE name = 'Nashik'),
    'flows_through'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Godavari') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Nashik') AND relationship_type = 'flows_through');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Krishna'),
    (SELECT id FROM graph_entities WHERE name = 'Satara'),
    'flows_through'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Krishna') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Satara') AND relationship_type = 'flows_through');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Ujani'),
    (SELECT id FROM graph_entities WHERE name = 'Solapur'),
    'located_in'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Ujani') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Solapur') AND relationship_type = 'located_in');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Koyna'),
    (SELECT id FROM graph_entities WHERE name = 'Satara'),
    'located_in'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Koyna') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Satara') AND relationship_type = 'located_in');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Sugarcane'),
    (SELECT id FROM graph_entities WHERE name = 'Kolhapur'),
    'grown_in'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Sugarcane') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Kolhapur') AND relationship_type = 'grown_in');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Cotton'),
    (SELECT id FROM graph_entities WHERE name = 'Solapur'),
    'grown_in'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Cotton') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Solapur') AND relationship_type = 'grown_in');

INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT 
    (SELECT id FROM graph_entities WHERE name = 'Soybean'),
    (SELECT id FROM graph_entities WHERE name = 'Nashik'),
    'grown_in'
WHERE NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = (SELECT id FROM graph_entities WHERE name = 'Soybean') AND target_id = (SELECT id FROM graph_entities WHERE name = 'Nashik') AND relationship_type = 'grown_in');

-- Link all districts to the State
INSERT INTO graph_relationships (source_id, target_id, relationship_type)
SELECT d.id, s.id, 'belongs_to'
FROM graph_entities d, graph_entities s
WHERE d.type = 'District' AND s.name = 'Maharashtra'
AND NOT EXISTS (SELECT 1 FROM graph_relationships WHERE source_id = d.id AND target_id = s.id AND relationship_type = 'belongs_to');
"""

with engine.connect() as conn:
    conn.execute(text(setup_sql))
    conn.execute(text(seed_sql))
    conn.commit()
print("✅ Knowledge Graph tables recreated and seeded successfully!")
