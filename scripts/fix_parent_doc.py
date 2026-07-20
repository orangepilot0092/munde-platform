import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import psycopg2
from src.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()

print("🔍 Inspecting document_registry schema...")
cur.execute("""
    SELECT column_name, data_type, is_nullable, column_default 
    FROM information_schema.columns 
    WHERE table_name = 'document_registry'
""")
schema = cur.fetchall()

cols = []
vals = []
placeholders = []

for col_name, dtype, nullable, default in schema:
    # Map the primary key / document ID
    if col_name in ("id", "document_id"):
        cols.append(col_name)
        vals.append(9999)
        placeholders.append("%s")
    # Fill in any other strictly required fields that have no default
    elif nullable == "NO" and default is None:
        cols.append(col_name)
        if "char" in dtype or "text" in dtype:
            vals.append("Maharashtra GR Jalyukt Shivar 2.0")
        elif "int" in dtype:
            vals.append(1)
        elif "timestamp" in dtype or "date" in dtype:
            vals.append("2024-01-01 00:00:00")
        else:
            vals.append("dummy")
        placeholders.append("%s")

if cols:
    sql = f"INSERT INTO document_registry ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
    print("💾 Inserting parent document...")
    try:
        cur.execute(sql, vals)
        conn.commit()
        print("✅ Parent document registered successfully!")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("✅ Parent document already exists.")
    except Exception as e:
        conn.rollback()
        print(f"⚠️ Error inserting: {e}")
else:
    print("⚠️ Could not find document_registry columns.")

cur.close()
conn.close()
