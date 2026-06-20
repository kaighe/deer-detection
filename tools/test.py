from ultralytics import YOLO

model = YOLO("model.pt")

results = model.predict(source="0", show=True)