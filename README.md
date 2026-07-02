# PPE Detection System

A real-time Personal Protective Equipment (PPE) detection system built using YOLOv8 and OpenCV. 
The system monitors a live camera feed and automatically detects whether people are wearing 
safety helmets. If a violation is found, it triggers an alert — a beep sound, a screenshot, 
a CSV log entry, and an email notification with the photo attached.

I built this project to understand how computer vision works in real-world safety applications, 
and to get hands-on experience with AI model training, real-time video processing, and 
full-stack integration.

---

## Dashboard Preview

![PPE Detection Dashboard](assets/dashboard.png)

---

## What it does

- Detects heads and helmets in real time using a webcam
- Flags violations when a person is detected without a helmet
- Plays a beep sound as an immediate on-site alert
- Saves a timestamped screenshot of every violation as evidence
- Logs all violations in a CSV file for compliance tracking
- Sends an automated email alert with the violation photo attached
- Displays everything on a live web dashboard built with Flask

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| YOLOv8 (Ultralytics) | Object detection model |
| OpenCV | Camera feed and video processing |
| Flask | Web dashboard backend |
| smtplib | Email alert system |
| python-dotenv | Secure credential management |
| CSV | Violation logging |
| HTML + CSS | Frontend dashboard UI |
| Roboflow | Training dataset source |
| Google Colab | Cloud GPU for model training |

---

## Project Structure

ppe-detection/

├── app.py               # Flask dashboard

├── detect.py            # Real-time detection + alert system

├── train.py             # Model training script

├── best.pt              # Trained YOLOv8 model

├── test_camera.py       # Camera test utility

├── templates/

│   └── index.html       # Dashboard HTML

├── static/

│   └── style.css        # Dashboard styling

├── assets/

│   └── dashboard.png    # Dashboard preview

└── .env.example         # Credential template 

---

## How to run this locally

**1. Clone the repository**
```bash
git clone https://github.com/Tirangini/ppe-detection-system.git
cd ppe-detection-system
```

**2. Install dependencies**
```bash
pip install ultralytics opencv-python flask python-dotenv pillow
```

**3. Set up your credentials**

Create a `.env` file in the root folder (this is excluded from GitHub for security):

EMAIL_ADDRESS=your_gmail@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
RECEIVER_EMAIL=receiver@gmail.com

To generate a Gmail App Password, go to myaccount.google.com → Security → App Passwords.

**4. Run the detection system**
```bash
python detect.py
```

**5. Run the web dashboard**
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

---

## Model Training

The YOLOv8n model was trained on the hard-hat-universe dataset from Roboflow — 
over 7,000 labeled construction site images across 3 classes: helmet, head, and person. 
Training was done on Google Colab using a T4 GPU for 25 epochs.

Final results:
- Helmet detection precision: 96.5%
- Head detection precision: 92.5%
- Overall mAP50: 65.1%

---

## Known Limitations

- The model occasionally misclassifies round objects (bowls, caps) as helmets due to 
  similar shape patterns in training data. This is a known false positive issue that 
  could be improved with a more diverse dataset.
- Currently detects helmets only — vest and gloves detection can be added by training 
  on a more comprehensive PPE dataset.

---

## Author

**Tirangini**
MCA Student — Babu Banarasi Das University, Lucknow
GitHub: https://github.com/Tirangini
