import serial
import cv2
import time
import os

# OneDrive Folder Path - Update if needed
ONEDRIVE_FOLDER = r"C:\Users\Han Lee\OneDrive - Georgia Institute of Technology\thieves"

# Ensure the directory exists
os.makedirs(ONEDRIVE_FOLDER, exist_ok=True)

# Connect to Arduino - Use higher baud rate for faster data transfer
SERIAL_PORT = "COM5"  # Change to the correct port
BAUD_RATE = 115200  # Increased from 9600 to 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)  # Lower timeout for faster response

# Initialize Webcam using DirectShow backend (cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("❌ Error: Could not open webcam")
    exit()

print("✅ System Ready. Listening for light alerts from Arduino...")

def capture_photo():
    """Captures a photo from the webcam and saves it in OneDrive."""
    ret, frame = cap.read()
    if ret:
        filename = f"light_alert_{int(time.time())}.jpg"
        filepath = os.path.join(ONEDRIVE_FOLDER, filename)
        cv2.imwrite(filepath, frame)
        print(f"📸 Image saved to OneDrive: {filepath}")
    else:
        print("⚠️ ERROR: Failed to capture image.")

# Main Loop: Listen to Arduino for "LIGHT_DETECTED" and capture image
while True:
    try:
        data = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore').strip()
        if "LIGHT_DETECTED" in data:
            print("🚨 Light detected! Capturing image instantly...")
            capture_photo()

        time.sleep(0.1)  # Faster check interval (was 0.5s, now 0.1s)

    except Exception as e:
        print(f"⚠️ ERROR: {e}")
        break

# Cleanup on exit
cap.release()
ser.close()
