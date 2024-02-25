import os

dataset_folder = '../dataset'

png_count = 0
tb_count = 0
dump_count = 0
number_of_folders = 0

for folder_name in os.listdir(dataset_folder):
    number_of_folders += 1
    folder_path = os.path.join(dataset_folder, folder_name)
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.png'):
                png_count += 1
            if file_name.endswith('tb.v'):
                tb_count += 1
            if file_name.endswith('dump.vcd'):
                dump_count += 1
print("Total number of folders: ", number_of_folders)
print("Total number of images: ", png_count)
print("Total number of testbenches: ", tb_count)
print("Total number of dump files: ", dump_count)

