from ultralytics import YOLO
import cv2
import time
import os
import csv
import winsound  # for beep sound (Windows only)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Load your trained model
model = YOLO("best.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Create a folder to save violation screenshots
if not os.path.exists("violations"):
    os.makedirs("violations")

# Create violations log file if it doesn't exist
log_file = "violations/violations_log.csv"
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Violation Type", "Screenshot"])

last_alert_time = 0  # to avoid spamming screenshots every frame

def send_email_alert(image_path, timestamp):
    msg = MIMEMultipart()
    msg['Subject'] = 'PPE Violation Alert - No Helmet Detected'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL

    body = MIMEText(f"A safety violation was detected at {timestamp}.\nNo helmet was detected on a person in the camera feed.")
    msg.attach(body)

    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename="violation.jpg")
        msg.attach(img)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email alert sent!")
    except Exception as e:
        print(f"Email failed: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()

    detected_classes = []
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        detected_classes.append(class_name)

    if "head" in detected_classes and "helmet" not in detected_classes:
        cv2.putText(annotated_frame, "VIOLATION: No Helmet!", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Only trigger alert once every 5 seconds (avoid spamming)
        current_time = time.time()
        if current_time - last_alert_time > 5:
            # Beep sound
            winsound.Beep(1000, 300)

            # Save screenshot with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            filename = f"violations/violation_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"Violation logged: {filename}")

            # Log the violation in CSV
            with open(log_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, "No Helmet", filename])

            # Send email alert
            send_email_alert(filename, timestamp)

            last_alert_time = current_time

    cv2.imshow("PPE Detection - Live", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()