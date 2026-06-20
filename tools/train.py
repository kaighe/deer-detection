from ultralytics import YOLO

def train_model():
    # 1. Load a pre-trained YOLO model (nano version is fast and efficient)
    model = YOLO("yolov8s.pt") 

    # 2. Train the model using your custom dataset configuration
    results = model.train(
        data="dataset/data.yaml",    # Path to your dataset configuration file
        epochs=100,           # Number of training rounds
        imgsz=640,           # Target image size resolution
        batch=32,            # Batch size (adjust based on GPU VRAM)
        device="cuda"
    )

if __name__ == "__main__":
    train_model()
