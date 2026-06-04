# 🧠 AI-Powered Medical Document Classifier (MedClassify)

> **Hackathon Submission** | Full-stack AI system that classifies medical documents in real-time using a fine-tuned Small Language Model (SLM), with live RAM monitoring and database persistence.

### 🌐 Live Deployments
- **Frontend Dashboard (Vercel)**: [https://image-classifier-ten.vercel.app/](https://image-classifier-ten.vercel.app/)
- **Backend API (Render)**: [https://image-classifier-xgu0.onrender.com](https://image-classifier-xgu0.onrender.com)
- **GitHub Repository**: [https://github.com/Nirucoder/image-classifier](https://github.com/Nirucoder/image-classifier)

---

## 📌 Features

- **4-Class Document Classification**: Handwritten Prescription, Printed Prescription, Printed Lab Report, Medical Scans (X-Ray/MRI)
- **Adaptive Binarization**: OpenCV-based preprocessing strips paper noise — the AI sees only ink strokes, drastically improving handwriting detection accuracy
- **Real-Time RAM Monitoring**: Tracks memory footprint (MB) per classification using `psutil`
- **Full PostgreSQL Persistence**: Every classification stores the filename, label, confidence, inference time, RAM usage, and the raw image binary in the database
- **History Dashboard**: View the last 10 classifications with all metrics in the UI

---

## 🏗️ Architecture

```
PROJECTS/
├── backend/                  # FastAPI + PyTorch inference engine
│   ├── app/
│   │   ├── main.py           # API endpoints (/classify, /history)
│   │   ├── engine.py         # ML model + Adaptive Binarization preprocessing
│   │   ├── models.py         # SQLAlchemy ORM (PostgreSQL table)
│   │   └── database.py       # DB connection & session management
│   ├── train.py              # Model fine-tuning script
│   ├── download_data.py      # Training data downloader
│   ├── check_db.py           # Manual DB inspector tool
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # React + Vite dashboard
│   └── src/app/
│       ├── App.tsx           # Main app logic & state
│       └── components/
│           ├── AnalysisResults.tsx  # Classification result cards
│           └── HistoryTable.tsx     # Historical records table
├── docker-compose.yml        # One-command full stack deployment
└── README.md
```

---

## 🤖 Model Justification

**Model: MobileNetV2** — a Convolutional Neural Network fine-tuned via transfer learning on a custom medical document dataset.

**Why MobileNetV2?**
- **Memory Optimized for Production**: MobileNetV2's small footprint uses **~370–380 MB RAM** on CPU locally and **<250 MB RAM** on Linux, preventing OOM crashes on Render's 512 MB free tier.
- **Ultra-Fast Inference**: Achieves **~30–80ms latency** on CPU (down from 150-200ms with EfficientNet).
- **Excellent Accuracy**: Fine-tuned on the medical dataset, the model yields **93.3% overall accuracy** on the same test dataset.
- **Adaptive Binarization Pre-processing**: OpenCV Otsu's thresholding transforms the input document into a high-contrast ink-only map, stripping shadow noise, so the neural network focuses solely on text stroke structure.

**Approximate Resource Usage:**
| Metric | Value |
|--------|-------|
| Model Size | ⚡ ~8.7 MB (weights file) |
| RAM per Inference | ~370–380 MB (RSS) |
| Inference Latency | ~30–80 ms (CPU) |
| GPU Required | ❌ No |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15 running locally

### 1. Clone the Repository
```bash
git clone https://github.com/Nirucoder/image-classifier.git
cd image-classifier
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your PostgreSQL password if different

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🐳 Docker Deployment (One Command)

Make sure Docker Desktop is running, then from the project root:

```bash
docker-compose up --build
```

This starts PostgreSQL, the FastAPI backend, and the React frontend automatically.

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🗄️ Database Verification

After classifying an image, verify it's stored in PostgreSQL:

```bash
cd backend
python check_db.py
```

Expected output:
```
============================================================
  🩺 MEDCLASSIFY - PostgreSQL Database Inspector
============================================================

  ID    Filename                       Result                     Conf%    RAM(MB)    Image Size     Time
  -----------------------------------------------------------------------------------------------------------------------
  1     prescription.jpg               Handwritten Prescription   91.2%    334.1      215.6 KB       2026-03-29 13:45:22
```

---

## 📡 API Reference

### `POST /classify`
Upload a medical document image for classification.

**Request**: `multipart/form-data` with `file` field

**Response**:
```json
{
  "prediction": "Handwritten Prescription",
  "confidence": 0.912,
  "latency": 183,
  "ram_mb": 334.1
}
```

### `GET /history`
Returns the last 10 classification records from PostgreSQL.

---

## 🔧 Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/medclassify_db
FRONTEND_URL=http://localhost:5173
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)
| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `torch` + `torchvision` | ML inference (CPU) |
| `opencv-python` | Adaptive Binarization preprocessing |
| `pillow` | Image loading |
| `sqlalchemy` | ORM for PostgreSQL |
| `psycopg2-binary` | PostgreSQL driver |
| `psutil` | RAM usage monitoring |

### Frontend
| Package | Purpose |
|---------|---------|
| `react` + `vite` | UI framework |
| `typescript` | Type safety |

---

## 👥 Team
Built for the **FULL STACK Intern Hackathon** — March 2026
