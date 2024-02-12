import os

# Specify the directory path
directory = 'dataset'

# Loop through the first level subfolders
for root, dirs, files in os.walk(directory):
    for file in files:
        # module name is the folder name
        module_name = os.path.basename(root)
        # remove all files except for module_name.v
        if not file.endswith(module_name + ".v"):
            # Construct the file path
            file_path = os.path.join(root, file)
            # Remove the file
            os.remove(file_path)