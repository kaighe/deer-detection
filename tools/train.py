from ultralytics import YOLO

def train_model():
    model = YOLO("yolov8s.pt") 

    results = model.train(
        data="datasets/main/data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        device="cuda"
    )

if __name__ == "__main__":
    train_model()