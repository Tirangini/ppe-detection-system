from ultralytics import YOLO
import cv2
import time
import os
import winsound  # for beep sound (Windows only)

# Load your trained model
model = YOLO("best.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Create a folder to save violation screenshots
if not os.path.exists("violations"):
    os.makedirs("violations")

last_alert_time = 0  # to avoid spamming screenshots every frame

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

            last_alert_time = current_time

    cv2.imshow("PPE Detection - Live", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()