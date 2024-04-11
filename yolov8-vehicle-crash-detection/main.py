# video2.py
import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import yaml

model = YOLO('./runs/detect/train4/weights/best.pt')
yaml_path = "data.yaml"
cap = cv2.VideoCapture('cr.mp4')

#재생할 파일의 넓이와 높이
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print("재생할 파일 넓이, 높이 : %d, %d"%(width, height))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (int(width), int(height)))

# Read class names from YAML file
with open(yaml_path, "r") as yaml_file:
    data = yaml.safe_load(yaml_file)
    class_list = data['names']


while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret == False:
        break
    
    results = model.predict(frame)

    for result in results:
        if result.boxes is not None and len(result.boxes.data) > 0:
            a = result.boxes.data.cpu().numpy()
            px = pd.DataFrame(a).astype("float")

            for index, row in px.iterrows():
                if any(pd.isna(row)):
                    continue

                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)

    cv2.imshow('frame',frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()