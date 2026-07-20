import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)

sql = """
-- 1. Add Multilingual Columns
ALTER TABLE metadata_registry ADD COLUMN IF NOT EXISTS name_mr VARCHAR(255);
ALTER TABLE metadata_registry ADD COLUMN IF NOT EXISTS name_hi VARCHAR(255);
ALTER TABLE metadata_registry ADD COLUMN IF NOT EXISTS description_mr TEXT;
ALTER TABLE metadata_registry ADD COLUMN IF NOT EXISTS description_hi TEXT;

-- 2. Seed Marathi Translations for existing datasets
UPDATE metadata_registry SET 
  name_mr = 'महाराष्ट्र जिल्हानिहाय पीक उत्पादन', 
  description_mr = 'महाराष्ट्रातील जिल्ह्यांमधील प्रमुख पिकांच्या वार्षिक उत्पादनाची आकडेवारी.'
WHERE dataset_id = 'maha_agri_001';

UPDATE metadata_registry SET 
  name_mr = 'महाराष्ट्रातील प्रमुख जलाशयांची पातळी', 
  description_mr = 'राज्यातील प्रमुख जलाशयांमधील दैनंदिन पाणीसाठ्याची पातळी.'
WHERE dataset_id = 'maha_water_001';

UPDATE metadata_registry SET 
  name_mr = 'MSRTC बस मार्ग आणि वेळापत्रक', 
  description_mr = 'MSRTC बस मार्ग, थांबे आणि नियोजित वेळांची संपूर्ण यादी.'
WHERE dataset_id = 'maha_transport_001';

-- 3. Rebuild search_vector using 'simple' config to preserve Devanagari tokens
UPDATE metadata_registry 
SET search_vector = to_tsvector('simple', 
    coalesce(name, '') || ' ' || coalesce(name_mr, '') || ' ' || coalesce(name_hi, '') || ' ' || 
    coalesce(description, '') || ' ' || coalesce(description_mr, '') || ' ' || coalesce(description_hi, '') || ' ' || 
    coalesce(domain, '') || ' ' || coalesce(tags::text, '')
);
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()
print("✅ Multilingual columns added, translations seeded, and search index rebuilt!")
