import cv2
import threading
import time
from datetime import datetime
from services.inference import get_model
from services.preprocessing import preprocess_frame
from services.realtime_state import current_state

model = get_model()

camera_lock = threading.Lock()
latest_frame = None
processed_frame = None


def inference_loop():
    global latest_frame, processed_frame

    while True:
        if latest_frame is None:
            time.sleep(0.05)
            continue

        with camera_lock:
            frame = latest_frame.copy()

        # 🔥 MODEL INFERENCE
        prob = float(model.predict(preprocess_frame(frame))[0][0])
        status = "FIRE" if prob > 0.5 else "SAFE"

        # ✅ SINGLE SOURCE OF TRUTH
        current_state["confidence"] = prob
        current_state["status"] = status
        current_state["lat"] = 11.0168
        current_state["lon"] = 76.9558
        current_state["updated_at"] = datetime.now().isoformat()

        # 🎥 Overlay for video (READS from current_state)
        overlay = frame.copy()
        color = (0, 0, 255) if status == "FIRE" else (0, 255, 0)

        cv2.putText(
            overlay,
            f"{status} {int(current_state['confidence'] * 100)}%",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )

        with camera_lock:
            processed_frame = overlay

        time.sleep(0.2)  # throttle inference



def generate_frames():
    global latest_frame, processed_frame

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        with camera_lock:
            latest_frame = frame.copy()
            frame_to_send = processed_frame if processed_frame is not None else frame

        success, buffer = cv2.imencode(".jpg", frame_to_send)
        if not success:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )
