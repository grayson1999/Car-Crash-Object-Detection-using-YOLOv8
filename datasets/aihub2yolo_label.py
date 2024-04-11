import json
import os
import shutil

##N 번째 다운로드
NUM = "1"

## 위치 변수
origin_path = "./origin_data/"
out_path = "./yolo_label/"

origin_folder_name = NUM + "_data"

##다운로드 폴더에서 origin 데이터 폴더로 옮기기
def download_to_origindata(origin_path, origin_folder_name):
    img_set_path = os.path.join(origin_path, origin_folder_name, "img_set")
    labelling_set_path = os.path.join(origin_path, origin_folder_name, "labelling_set")

    os.makedirs(img_set_path, exist_ok=True)
    os.makedirs(labelling_set_path, exist_ok=True)

    download_folders = os.listdir(f"./download_data/{NUM}_set_download/")

    for name in download_folders:
        if name.endswith("zip"):
            continue
        elif name.find("TS") != -1:
            shutil.move(f"./download_data/{NUM}_set_download/{name}/", os.path.join(img_set_path, name))
        elif name.find("TL") != -1:
            shutil.move(f"./download_data/{NUM}_set_download/{name}/", os.path.join(labelling_set_path, name))

def origin2yolo(json_file_path):
    # Open the JSON file and read its contents
	with open(json_file_path, 'r') as file:
		json_data = file.read()

	data = json.loads(json_data)

	# YOLO 클래스 매핑
	class_mapping = {
		"accident": 0,
		"vehicle": 1,
		"pedestrian": 2,
		"two-wheeled-vehicle": 3,

	}

	# YOLO 형식으로 변환한 결과를 담을 리스트
	yolo_labels = []

	# 객체들에 대한 반복문
	for obj in data["objects"]:
		# 카테고리에 따라 YOLO 클래스 할당
		category = obj["category"]
		
		## 사고인 경우 accident
		if obj["isObjectA"] or obj["isObjectB"]:
			class_id = class_mapping["accident"]
		
		## categ
		elif category in class_mapping:
			class_id = class_mapping[category]
		else:
			continue

		# bounding box 좌표
		x_center = (obj["bbox"][0] + obj["bbox"][2] / 2) / data["width"]
		y_center = (obj["bbox"][1] + obj["bbox"][3] / 2) / data["height"]
		width = obj["bbox"][2] / data["width"]
		height = obj["bbox"][3] / data["height"]

		# YOLO 형식으로 변환한 결과 추가
		yolo_labels.append([class_id, x_center, y_center, width, height])

	# 변환 결과 출력
	return yolo_labels

def save_yolo_label_txt(out_path, file_name, result_list):
	file_name = file_name.split(".")[0]
	out_path = f"{out_path}labels/"
	os.makedirs(out_path, exist_ok = True)

	with open(f"{out_path}{file_name}.txt", "w") as f:
		for label in result_list:
			f.write(" ".join(str(item) for item in label) + "\n")

#main
download_to_origindata(origin_path, origin_folder_name)


origin_label_path = origin_path+origin_folder_name+"/labelling_set/"
dir_list = os.listdir(origin_label_path)

print("-"*5+"라벨링 변환 시작"+"-"*5)
for dir in dir_list:
	sub_folders = os.listdir(origin_label_path+dir)
	for sub_folder in sub_folders:
		files = os.listdir(origin_label_path+dir+"/"+sub_folder)
		for file in files:
			yolo_labels = origin2yolo(origin_label_path+dir+"/"+sub_folder+"/"+file)
			save_yolo_label_txt(out_path,file,yolo_labels)


origin_img_path = origin_path+origin_folder_name+"/img_set/"
dir_list = os.listdir(origin_img_path)

print("-"*5+"이미지 이동 시작"+"-"*5)
for dir in dir_list:
	sub_folders = os.listdir(origin_img_path+dir)
	for sub_folder in sub_folders:
		files = os.listdir(origin_img_path+dir+"/"+sub_folder)
		for file in files:
			os.makedirs(out_path+"images", exist_ok=True)
			shutil.move(origin_img_path+dir+"/"+sub_folder+"/"+file, out_path+"images/"+file)
