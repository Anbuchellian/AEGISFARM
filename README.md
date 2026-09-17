# AEGISFARM — 35% Project Software Prototype

**Adaptive AI Invisible Fence for Autonomous Crop Protection**

This repository implements the software scope described in the 35% Project Better Tomorrow report:

> Detect → Identify → Predict → Deter → Observe → Adapt → Verify → Learn

## What is included

- FastAPI backend
- SQLite by default; PostgreSQL via `DATABASE_URL`
- YOLO integration hook (optional model file)
- ByteTrack-capable tracking hook
- Demo/simulation detection mode with realistic farm events
- Zone-based risk scoring
- Safety-constrained adaptive response engine
- Response memory and intervention history
- Farmer-friendly React dashboard
- Event timeline and risk heatmap
- Validation/testing screen
- Optional MQTT bridge and ESP32 example
- Windows and Linux/macOS run scripts

## Prototype boundary

This package is an **engineering prototype** for a 35% submission. The default demo mode does not claim field accuracy. Real model performance, deterrent effectiveness, user feedback, and field success rates must be measured and entered only after testing.

## 1. Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend: http://localhost:8000
API docs: http://localhost:8000/docs

## 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## 3. One-click scripts

Windows:
- `scripts\\run_backend.bat`
- `scripts\\run_frontend.bat`

Linux/macOS:
- `scripts/run_backend.sh`
- `scripts/run_frontend.sh`

## 4. Demo workflow

Open the dashboard and click **Simulate Intrusion**. AEGISFARM creates an event, runs risk assessment, selects a response strategy, and records the intervention. Use **Simulate No Response** to demonstrate adaptive retry and response memory.

## 5. Real YOLO inference

Install the optional package:

```bash
pip install ultralytics
```

Place a compatible model file such as `yolo11n.pt` or a project-trained animal model in `backend/models/` and set:

```env
MODEL_PATH=models/yolo11n.pt
```

For best results, train/fine-tune the model on the exact animal classes relevant to the field test. The demo simulator remains available without weights.

## 6. Optional PostgreSQL

Set:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/aegisfarm
```

The code otherwise uses SQLite so the prototype runs with zero database setup.

## 7. Scope mapping to the 35% report

| Report requirement | Software module |
|---|---|
| Detect | `services/detection.py` |
| Identify | `services/detection.py` |
| Track | `services/tracking.py` |
| Predict | `services/risk.py` |
| Deter | `services/response_engine.py` |
| Observe | `services/observation.py` |
| Adapt | `services/response_engine.py` |
| Verify | `services/observation.py` |
| Learn | `services/memory.py` |
| Farmer dashboard | `frontend/` |
| Validation | `api/validation.py` + UI |
| IoT/MQTT | `services/mqtt_bridge.py` |
| ESP32 example | `hardware/esp32/` |

## Important safety note

The response layer is intentionally implemented as **safe, configurable actions** such as alert state, directional-light placeholder, and approved audio strategy identifiers. Do not connect hazardous equipment or deploy wildlife deterrence without species-specific testing and applicable approvals.
