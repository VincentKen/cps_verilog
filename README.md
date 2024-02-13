To generate the training data use the following scripts in the correct order:  
### 1 generate_dataset.py
generate_dataset.py will download verilog code from huggingface from the wangxinze/Verilog_data dataset. Each entry in this dataset is a verilog module. This script creates the "dataset" folder, and then for each verilog module it will create a subfolder where the name of that folder is the name of the module. 
In each of the module's folder it will place a verilog file containing the code for that module. The name of that file is the module name followed by `.v`. In the end the structure looks like `dataset/a_verilog_module_name/a_verilog_module_name.v`.

### 2 generate_testbenches.py
Before running this script, run the `vlogtbgen/setup_env.bat` script at least once in the current command window to set the proper environment variables to use vlogtbgen. vlogtbgen is one of the tools used to generate testbenches for the verilog modules.
The generate_testbenches.py script will go through the subfolders of `dataset` and attempts to generate a testbench for each of the verilog modules. It does this by first trying to run vlogtbgen, if this tools fails to generate a testbench, it will attempt the testbench_generator.py script.  
Each testbench is stored in `dataset/a_verilog_module_name/a_verilog_module_name_tb.v`.

### 3 generate_simulations.py
The generate_simulations.py script uses xvlog, xelab, and xsim to generate a vcd file with the results of the simulation which was run on the previously generate testbenches. This vcd file is stored in `dataset/a_verilog_module_name/dump.vcd`.

### 4 generate_waveforms.py
The generate_waveforms.py script uses the previously generated vcd file to generate timing diagrams using wavedrom. This script has two prerequisites, first the wavedrom-cli node package needs to be installed, secondly, vcd2wavedrom needs to be installed. vcd2wavedrom can be installed by going into vcd2wavedrom and running  `pip install .`.  
This script generates `dataset/a_verilog_module_name/timingdiagram.png` file for every module with a correct vcd file.

### Other scripts  
 - dataset_count.py counts the total amount of subfolders in `dataset`, the total amount of testbenches, the amount of vcd files, and the amount of timing diagrams.
 - reset_dataset.py removes all files from the `dataset` folder generated after step 1, so only the main `a_verilog_module_name.v` files will remain.
