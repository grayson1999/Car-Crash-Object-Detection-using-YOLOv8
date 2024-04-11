import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import yaml

model=YOLO('./runs/detect/train4/weights/best.pt')
cap=cv2.VideoCapture('./cp_1.mp4')
yaml_path = "data.yaml"


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        point = [x, y]
        print(point)
  
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)


# yaml 파일 읽기
with open(yaml_path, "r") as yaml_file:
    data = yaml.safe_load(yaml_file)

# dictionary 형태로 변환된 class_list
class_list = data['names']

count=0

while True:    
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
   
    count += 1
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)

    for result in results:  # 각 결과에 대해 반복
        if result.boxes is not None and len(result.boxes.data) > 0:  # 객체가 감지되었는지 확인
            a = result.boxes.data.cpu().numpy()
            px = pd.DataFrame(a).astype("float")

            for index, row in px.iterrows():
                if any(pd.isna(row)):  # NaN이 있는지 확인
                    continue  # NaN이 포함된 행을 건너뜁니다.

                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                
                # print("class_list ",end="")
                # print(class_list)
                # print("d "+str(d))
                # print("c "+c)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)
            
    
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()  
cv2.destroyAllWindows()





