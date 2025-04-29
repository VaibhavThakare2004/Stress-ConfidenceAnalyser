import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# === CONFIGURATION ===
ENABLE_GUI = True  # Set to True if running in an IDE with GUI support

# === LOAD MODEL ===
model = load_model(r"C:\Users\vaibh\Desktop\Work\stress\Train\emotion_model2.h5")

# === CONSTANTS ===
IMG_SIZE = 48
EMOTIONS = ["Angry", "Determined", "Disgust", "Excited", "Fear", "Happy", "Neutral", "Surprise", "Sad", "Proud"]
CONFIDENCE_MAP = {
    "Angry": "Underconfident",
    "Determined": "Confident",
    "Disgust": "Underconfident",
    "Excited": "Confident",
    "Fear": "Underconfident",
    "Happy": "Confident",
    "Neutral": "Neutral",
    "Proud": "Confident",
    "Sad": "Underconfident",
    "Surprise": "Neutral"
}

# === FACE DETECTOR ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# === LOAD VIDEO ===
video_path = r"C:\Users\vaibh\Desktop\Work\stress\Train\output_video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Error: Could not open video.")
    exit()

# Get the video frame width, height, and FPS
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the output file name (add "-final" to the original video name)
output_video_path = video_path.replace(".mp4", "-final.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other formats like 'XVID', 'MJPG', etc.
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

frame_count = 0
result_data = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    frame_count += 1

    # Process every 5 seconds if face is detected
    if frame_count % (5 * fps) == 0 and len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y + h, x:x + w]
        face_resized = cv2.resize(face_roi, (IMG_SIZE, IMG_SIZE))
        face_normalized = face_resized / 255.0
        face_input = np.reshape(face_normalized, (1, IMG_SIZE, IMG_SIZE, 1))

        prediction = model.predict(face_input, verbose=0)[0]
        predicted_index = np.argmax(prediction)
        emotion = EMOTIONS[predicted_index]
        confidence_level = CONFIDENCE_MAP[emotion]

        # Time interval
        interval_start = ((frame_count // (5 * fps)) - 1) * 5
        interval_end = interval_start + 5
        timestamp = f"{interval_start}-{interval_end}"

        result_data.append([timestamp, emotion, confidence_level])

    # Optional live drawing of rectangles around faces and emotion labels
    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        face_resized = cv2.resize(face_roi, (IMG_SIZE, IMG_SIZE))
        face_normalized = face_resized / 255.0
        face_input = np.reshape(face_normalized, (1, IMG_SIZE, IMG_SIZE, 1))

        prediction = model.predict(face_input, verbose=0)[0]
        predicted_index = np.argmax(prediction)
        emotion = EMOTIONS[predicted_index]
        confidence_level = CONFIDENCE_MAP[emotion]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"{emotion} ({confidence_level})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    if ENABLE_GUI:
        # Display the frame in the GUI
        cv2.imshow("Emotion Confidence Detection", frame)

    # Write the frame to the output video
    out.write(frame)
    
    # Wait for 30ms and break if 'q' is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
out.release()  # Release the video writer

if ENABLE_GUI:
    cv2.destroyAllWindows()

# === SAVE RESULTS ===
df = pd.DataFrame(result_data, columns=["Time (s)", "Emotion", "Confidence Level"])
output_csv = "emotion_confidence_results.csv"
df.to_csv(output_csv, index=False)
print(f"✅ Results saved to {output_csv}")
print(f"✅ Video saved as {output_video_path}")
