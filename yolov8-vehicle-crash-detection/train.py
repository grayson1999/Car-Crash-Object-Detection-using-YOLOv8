from ultralytics import YOLO
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

def train():
    # Load a model
    model = YOLO('yolov8s.pt')  # load a pretrained model (recommended for training)
    # model = YOLO('yolov8s.yaml').load('yolov8s.pt')  # build from YAML and transfer weights

    # Train the model
    results = model.train(data='./data_1.yaml', epochs=80, imgsz=640, batch=8)

if __name__ == "__main__":
    train()