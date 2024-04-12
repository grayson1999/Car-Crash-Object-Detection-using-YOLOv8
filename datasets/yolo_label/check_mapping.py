import os 
image_files = os.listdir('./images')
label_fils = os.listdir('./labels')

image_list = []
labels_list = []
for image_name in image_files:
    image_list.append(image_name[:-4])
for label_name in label_fils:
    labels_list.append(label_name[:-4])


for name in image_list:
    if name in labels_list:
        pass
    else:
        print(name, end=', ')
