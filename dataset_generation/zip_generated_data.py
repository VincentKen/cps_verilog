import os
import zipfile

def gather_folders_with_png_files(dataset_folder, zip_file_path):
    subfolders = [f.path for f in os.scandir(dataset_folder) if f.is_dir()]
    files_to_be_zipped = []
    for subfolder in subfolders:
        files = [f.name for f in os.scandir(subfolder) if f.is_file()]
        add_files = False
        if any(file.endswith('.png') for file in files):
            add_files = True
        if add_files:
            # add any file ending with .v, .png, .vcd and timer.json
            files_to_be_zipped += [os.path.join(subfolder, file) for file in files if file.endswith('.v') or file.endswith('.png') or file.endswith('.vcd') or file.endswith('timer.json')]
    # create a zip file and add all folders with png files
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for file in files_to_be_zipped:
            zip_file.write(file)

# Usage example:
dataset_folder = 'datasets'
zip_file_path = 'dataset.zip'
gather_folders_with_png_files(dataset_folder, zip_file_path)
