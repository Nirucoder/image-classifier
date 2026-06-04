import os
import time
import gc
import psutil
import torch
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import ClassificationHistory
from .engine import predict_image

# Initialize DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# IMPORTANT: Allow your React frontend to talk to this API
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/classify")
async def classify_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    start_time = time.time()
    image_data = await file.read()
    
    # 1. Run the AI engine
    label, confidence = predict_image(image_data)
    
    # 2. Guard against non-medical images (Confidence Threshold)
    # Lowered to 0.30 for Demo flexibility
    if confidence < 0.30:
        label = "Invalid/Non-Medical"
        
    # 3. Capture memory usage
    process = psutil.Process(os.getpid())
    ram_mb = float(process.memory_info().rss / 1024 / 1024)
    
    latency = int((time.time() - start_time) * 1000)
    
    # 2. CREATE the database record
    new_entry = ClassificationHistory(
        filename=file.filename,
        prediction=label,
        confidence=confidence,
        latency_ms=latency,
        ram_mb=ram_mb,
        image_data=image_data
    )
    
    # 3. SAVE to PostgreSQL
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    # 4. Release Memory Immediately
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

    return {"prediction": label, "confidence": confidence, "latency": latency, "ram_mb": ram_mb}

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    # Fetch the 10 most recent classifications (excluding the large binary image_data)
    records = db.query(
        ClassificationHistory.id,
        ClassificationHistory.filename,
        ClassificationHistory.prediction,
        ClassificationHistory.confidence,
        ClassificationHistory.latency_ms,
        ClassificationHistory.ram_mb,
        ClassificationHistory.created_at
    ).order_by(ClassificationHistory.created_at.desc()).limit(10).all()
    
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "prediction": r.prediction,
            "confidence": r.confidence,
            "latency_ms": r.latency_ms,
            "ram_mb": r.ram_mb,
            "created_at": r.created_at
        }
        for r in records
    ]