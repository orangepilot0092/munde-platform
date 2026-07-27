"""
Knowledge Layer: Generate and store vector embeddings for Intelligence Assets.
Uses a local, lightweight sentence-transformers model (384 dimensions).
"""
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from munde.core.models import IntelligenceAsset

print("📥 Loading local embedding model (all-MiniLM-L6-v2, 384 dims)...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded successfully!")

def generate_and_store_embeddings():
    print("🚀 Starting embedding generation for Intelligence Assets...")
    
    db_url = "postgresql+psycopg2://munde:munde_dev_password@192.168.29.20:5432/munde_core"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    
    with Session() as session:
        # Fetch all assets that don't have an embedding yet
        assets = session.query(IntelligenceAsset).filter(IntelligenceAsset.embedding == None).all()
        print(f"📊 Found {len(assets)} Intelligence Assets to embed.")
        
        for asset in assets:
            text_content = f"{asset.name}. {asset.description or ''}"
            
            # Generate 384-dimensional embedding locally
            embedding_vector = model.encode(text_content).tolist()
            
            if embedding_vector:
                # Update the database using raw SQL to handle pgvector casting safely
                update_stmt = text("""
                    UPDATE intelligence_assets 
                    SET embedding = CAST(:emb AS vector) 
                    WHERE id = :asset_id
                """)
                session.execute(update_stmt, {
                    "emb": str(embedding_vector),
                    "asset_id": asset.id
                })
                print(f"✅ Embedded: {asset.name} (dimensions: {len(embedding_vector)})")
            else:
                print(f"❌ Failed to generate embedding for: {asset.name}")
        
        session.commit()
    
    print("💾 Embedding generation complete!")

if __name__ == "__main__":
    generate_and_store_embeddings()
