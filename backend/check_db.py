import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print("\n" + "="*60)
    print("  🩺 MEDCLASSIFY - PostgreSQL Database Inspector")
    print("="*60)

    result = connection.execute(text("""
        SELECT id, filename, prediction, confidence, latency_ms, ram_mb,
               LENGTH(image_data) AS image_bytes, created_at
        FROM classification_history
        ORDER BY created_at DESC
        LIMIT 10
    """))

    records = result.fetchall()

    if not records:
        print("\n  No records found. Classify an image first!")
    else:
        print(f"\n  {'ID':<5} {'Filename':<30} {'Result':<25} {'Conf%':<8} {'RAM(MB)':<10} {'Image Size':<15} {'Time'}")
        print("  " + "-"*115)
        for row in records:
            img_size = f"{row[6] / 1024:.1f} KB" if row[6] else "N/A"
            conf_pct = f"{row[3]*100:.1f}%"
            print(f"  {row[0]:<5} {(row[1] or 'N/A'):<30} {row[2]:<25} {conf_pct:<8} {row[5]:<10.1f} {img_size:<15} {row[7]}")

    print("\n" + "="*60 + "\n")
