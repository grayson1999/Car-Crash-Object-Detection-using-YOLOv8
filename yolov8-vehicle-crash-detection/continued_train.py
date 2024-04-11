from ultralytics import YOLO


def continued_train():
    # Load a model
    model = YOLO('./runs/detect/train4/weights/last.pt')  # load a partially trained model

    # Resume training
    results = model.train(resume=True)

if __name__ == "__main__":
    continued_train()
