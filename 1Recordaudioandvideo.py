import cv2
import pyaudio
import wave
import time
import os

# Parameters
FRAME_WIDTH, FRAME_HEIGHT = 640, 480
FPS = 20  # Video frame rate
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # CD-quality audio
CHUNK = int(RATE / FPS)  # Dynamically adjust chunk size for perfect sync

# Output files
VIDEO_FILE = "output_video.mp4"
AUDIO_FILE = "output_audio.wav"
FINAL_OUTPUT = "final_output.mp4"

# Initialize Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

# Initialize Video Writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(VIDEO_FILE, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

# Initialize Audio Recording
audio = pyaudio.PyAudio()
audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
audio_frames = []

print("Recording started... Press 'q' to stop.")

start_time = time.time()

while True:
    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    # Capture audio
    audio_data = audio_stream.read(CHUNK, exception_on_overflow=False)
    audio_frames.append(audio_data)

    # Save video frame
    video_writer.write(frame)

    frame = cv2.flip(frame,1)
    # Show live video
    cv2.imshow("Recording Video", frame)

    # Stop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop video recording
cap.release()
cv2.destroyAllWindows()

# Stop audio recording
audio_stream.stop_stream()
audio_stream.close()
audio.terminate()

# Save audio file
with wave.open(AUDIO_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_frames))

# Save video file
video_writer.release()
