import os
import shutil

# Path to the dataset folder
dataset_folder = "dataset"

# Path to the folder where testbench files will be moved
testbench_folder = "dataset_with_testbenches"

# Loop through the dataset folders
for folder in os.listdir(dataset_folder):
    # Construct the path to the folder
    folder_path = os.path.join(dataset_folder, folder)
    # if folder contains a file ending with tb.v
    if any(filename.endswith("tb.v") for filename in os.listdir(folder_path)):
        folder_name = os.path.basename(folder_path)
        print(folder_name)
        new_folder = os.path.join(testbench_folder, folder_name)
        os.makedirs(new_folder, exist_ok=True)
        for file in os.listdir(folder_path):
            if file.endswith("tb.v") or file.endswith("{}.v".format(folder_name)):
                file_path = os.path.join(folder_path, file)
                shutil.copy(file_path, new_folder)