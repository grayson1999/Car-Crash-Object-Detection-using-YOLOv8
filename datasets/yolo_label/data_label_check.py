import os
import cv2


NUM="1"

CLASS_MAPPING = {		  
    "0": "accident",
    "1": "vehicle",
    "2": "pedestrian",
    "3": "two-wheeled-vehicle",
}

def draw_bbox(image, bbox_list):
    for bbox in bbox_list:
        class_id, x_center, y_center, width, height = bbox
        class_id = str(class_id)
        class_name = CLASS_MAPPING.get(class_id, "Unknown")
        x_center = int(float(x_center) * image.shape[1])
        y_center = int(float(y_center) * image.shape[0])
        width = int(float(width) * image.shape[1])
        height = int(float(height) * image.shape[0])
        x1 = x_center - width // 2
        y1 = y_center - height // 2
        x2 = x_center + width // 2
        y2 = y_center + height // 2
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

dir_path = "./".format(NUM)
dir_list = os.listdir(dir_path)

images_folder = "train/images"
labels_folder = "train/labels"

images_path = os.path.join(dir_path, images_folder)
labels_path = os.path.join(dir_path, labels_folder)

for image_file in os.listdir(images_path):
    if image_file.endswith(".png"):
        image_path = os.path.join(images_path, image_file)
        txt_file = os.path.join(labels_path, image_file[:-4] + ".txt")
        image = cv2.imread(image_path)
        with open(txt_file, "r") as f:
            bbox_list = [line.strip().split() for line in f]
            bbox_list = [[int(float(bbox[0])), *map(float, bbox[1:])] for bbox in bbox_list]  # Convert to desired format
        draw_bbox(image, bbox_list)
        cv2.imshow("image", image)
        cv2.waitKey(0)

cv2.destroyAllWindows()