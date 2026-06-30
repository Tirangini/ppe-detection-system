from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="hard-hat-universe.v1-1.yolov8/data.yaml",
    epochs=25,
    imgsz=640,
    batch=8,
    name="ppe_model"
)

print("Training complete!")