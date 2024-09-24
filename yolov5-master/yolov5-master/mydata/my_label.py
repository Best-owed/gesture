import xml.etree.ElementTree as ET
import os
from os import getcwd

sets = ['train', 'val', 'test']
classes = ["A", "B", "C", "D"]  # 确保与实际类别一致
abs_path = getcwd()
print("Current working directory:", abs_path)


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x * dw, y * dh, w * dw, h * dh


def convert_annotation(image_id):
    print(f"Converting annotation for: {image_id}")
    try:

        in_file_path = os.path.join('Annotations', f'{image_id}.xml')
        out_file_path = os.path.join('labels', f'{image_id}.txt')

        if not os.path.exists(in_file_path):
            print(f"Annotation file {in_file_path} does not exist.")
            return

        in_file = open(in_file_path, encoding='UTF-8')
        out_file = open(out_file_path, 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        print(f"Image size: width={w}, height={h}")

        object_count = 0
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            object_count += 1
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(f"{cls_id} {' '.join(map(str, bb))}\n")

        print(f"Found {object_count} objects in {image_id}.")
    except Exception as e:
        print(f"Error processing {image_id}: {e}")


if not os.path.exists('labels'):
    os.makedirs('labels')

for image_set in sets:

    image_set_path = os.path.join('ImageSets', 'Main', f'{image_set}.txt')
    if not os.path.exists(image_set_path):
        print(f"Image set file {image_set_path} does not exist.")
        continue

    image_ids = open(image_set_path).read().strip().split()
    print(f"Processing image set: {image_set}, Image IDs: {image_ids}")
    print(image_ids)
    list_file = open(f'{image_set}.txt', 'w')
    for image_id in image_ids:
        list_file.write(os.path.join(abs_path, 'images', f'{image_id}.jpg') + '\n')
        convert_annotation(image_id)
    list_file.close()
