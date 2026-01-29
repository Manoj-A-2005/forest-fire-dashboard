# 🌲 Smart Forest Fire Surveillance System

**Real-Time Fire Detection • Live Video • Heat Map • Alerts**

## 📌 Project Overview

The **Smart Forest Fire Surveillance System** is a real-time monitoring application designed to detect forest fires using  **live video streams and deep learning** , visualize detected fire zones on an  **interactive map** , and send **instant alerts** via Telegram.

This project integrates:

* **Computer Vision (CNN / Transfer Learning)**
* **FastAPI backend**
* **WebSocket-based real-time updates**
* **Live MJPEG video streaming**
* **Interactive Leaflet heat maps**
* **Modern Material UI–styled frontend**

The system is suitable for  **smart city** ,  **environmental monitoring** , and **disaster prevention** use cases.

## 🎯 Key Features

* 🔥 **Real-time fire detection** from live camera feed
* 🎥 **Stable MJPEG video streaming** (no UI crash)
* 📊 **Live confidence score** synced with video inference
* 🗺️ **Live map marker & heat zone visualization**
* 🚨 **Alert banner when fire is detected**
* 🤖 **Telegram alert integration** (manual / automatic)
* ⚡ **WebSocket-based real-time updates (no polling)**
* 🎨 **Responsive Material Design UI with forest theme**

## 🧠 System Architecture

```
Camera Feed
    ↓
OpenCV Video Capture
    ↓
Deep Learning Model (TensorFlow)
    ↓
Shared Realtime State
    ↓
 ┌──────────────┬───────────────┐
 │ MJPEG Stream │ WebSocket Push │
 └──────────────┴───────────────┘
        ↓                  ↓
   Live Video UI     Confidence + Map + Alerts
```

## 📂 Project Folder Structure

```
forest-fire-live-dashboard/
│
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── db.py                   # SQLite database setup
│   ├── requirements.txt        # Backend dependencies
│   ├── .gitignore              # Backend git ignore rules
│   │
│   ├── services/
│   │   ├── video_stream.py     # MJPEG video streaming + inference
│   │   ├── inference.py        # Model loading (TensorFlow)
│   │   ├── preprocessing.py    # Frame preprocessing
│   │   ├── realtime_state.py   # Shared realtime state
│   │
│   ├── model/
│   │   └── transfer_learned_model.h5  # Fire detection model
│
├── frontend/
│   ├── index.html              # Dashboard UI
│   ├── style.css               # Styling & animations
│   ├── script.js               # WebSocket, map & UI logic
│   └── assets/
│       └── forest-bg.jpg       # Background image
│
└── README.md                   # Project documentation
```

## 🔍 Backend Module Description

### `main.py`

* Initializes **FastAPI**
* Starts inference thread on startup
* Serves:
  * `/video-feed` → MJPEG live stream
  * `/ws/realtime` → WebSocket real-time data
  * `/send-telegram-alert` → Telegram notification

### `video_stream.py`

* Captures camera frames using OpenCV
* Runs ML inference in a **background thread**
* Uses thread locks to avoid frame corruption
* Overlays fire status & confidence on video
* Updates shared `current_state`

### `realtime_state.py`

Acts as a  **single source of truth** :

```python
current_state = {
  "confidence": 0.0,
  "status": "SAFE",
  "lat": 11.0168,
  "lon": 76.9558,
  "updated_at": ""
}
```

Used by:

* Video overlay
* WebSocket
* Map visualization
* UI confidence cards

### `inference.py`

* Loads the trained **transfer learning model**
* Ensures model is loaded **only once**

### `preprocessing.py`

* Resizes frames
* Normalizes pixel values
* Converts frames into model-ready tensors

## 🎨 Frontend Module Description

### `index.html`

* Material Design layout
* Live video panel
* Interactive map panel
* Zone confidence cards
* Telegram alert button

### `script.js`

* WebSocket connection (`/ws/realtime`)
* Real-time UI updates
* Live Leaflet marker & heat map
* Alert trigger logic

### `style.css`

* Forest-themed green palette
* Glassmorphism cards
* Smooth animations
* Fully responsive layout

## 🗺️ Live Map & Heat Zone Logic

* Uses **Leaflet.js**
* Marker color:
  * 🟢 Green → SAFE
  * 🔴 Red → FIRE
* Heat intensity = model confidence
* Updates are **throttled** to prevent UI lag

## 🤖 Telegram Alert Integration

* Secure backend-only bot token usage
* Triggered via button or automatically on FIRE
* Message includes:
  * Fire status
  * Confidence
  * Time
  * Zone

## ⚙️ Setup Guide (Local Installation)

### 🔹 Prerequisites

* Python **3.9 – 3.11**
* Webcam
* Git
* Virtual environment support

### 🔹 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install "uvicorn[standard]"
```

### 🔹 Start Backend Server

```bash
uvicorn main:app
```

Server runs at:

```
http://127.0.0.1:8000
```

### 🔹 Frontend Setup

Open directly in browser:

```
frontend/index.html
```

(No build step required)

## 🧪 Testing Checklist

* [X] Live video loads
* [X] Confidence changes in Zone A
* [X] Map marker updates
* [X] Heat zone intensity changes
* [X] Alert banner triggers
* [X] Telegram alert sends

## 🔐 Security Notes

* Telegram bot token stored **only in backend**
* `.env` and models excluded from Git
* WebSocket used instead of polling

## 🚀 Future Enhancements

* Multiple camera feeds
* Fire spread prediction
* Historical fire analytics
* Cloud deployment (Docker + AWS)
* SMS / Email alerts
* Mobile app integration

“The system detects fire from live video using a deep learning model, streams video independently to avoid UI blocking, synchronizes confidence and map updates using WebSockets, and provides real-time visualization and alerting.”
