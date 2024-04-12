from glob import glob
import yaml
import os
import shutil




dataset_path = "../datasets/yolo_label"

img_list = glob(dataset_path+"/images/*.jpg")
label_list = glob(dataset_path+"/labels/*.txt")

print(len(img_list),len(label_list))

## 학습, 검증 데이터 분리
from sklearn.model_selection import train_test_split
train_img_list, val_img_list = train_test_split(img_list, test_size=0.2,random_state=2000)
print(train_img_list)

##train, valid 폴더 생성
folder_names = ["train", "valid"]

for folder_name in folder_names:
    folder_path = os.path.join(dataset_path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

    subfolders = ["images", "labels"]
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.exists(subfolder_path):
            os.mkdir(subfolder_path)
            print(f"Created subfolder: {subfolder_path}")
        else:
            print(f"Subfolder already exists: {subfolder_path}")


for train_img in train_img_list:
    src_path, name = "/".join(train_img.split("/")[:-1]),train_img.split("/")[-1]
    name = name[:-4]
    shutil.move(src_path+"/"+name+".jpg",dataset_path+"/train/images/"+name+".jpg")
    shutil.move(dataset_path+"/labels/"+name+".txt",dataset_path+"/train/labels/"+name+".txt")

for val_img in val_img_list:
    src_path, name = "/".join(val_img.split("/")[:-1]),val_img.split("/")[-1]
    name = name[:-4]
    shutil.move(src_path+"/"+name+".jpg",dataset_path+"/valid/images/"+name+".jpg")
    shutil.move(dataset_path+"/labels/"+name+".txt",dataset_path+"/valid/labels/"+name+".txt")



#ymal 파일 수정
with open("./data_1.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

data['train'] = '/app/datasets/yolo_label/train/images/'
data['val'] = '/app/datasets/yolo_label/valid/images/'

with open("./data.yaml","w") as f:
    yaml.dump(data,f)

print(data)