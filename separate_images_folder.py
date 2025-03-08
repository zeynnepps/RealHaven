import os
import shutil

source_folder = "/Users/zeynepsalihoglu/Downloads/RealHaven/House_Room_Dataset/Livingroom"
destination_folder = "/Users/zeynepsalihoglu/Downloads/RealHaven/house_detailed_images/livingroom"

os.makedirs(destination_folder, exist_ok=True)

image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

selected_images = image_files[:500]

for i, filename in enumerate(selected_images, start=1):
    new_name = f"living_{i}{os.path.splitext(filename)[1]}" 
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, new_name)
    
    shutil.copy(source_path, destination_path)

print("500 images renamed and copied successfully.")
