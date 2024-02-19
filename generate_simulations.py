import time
import os
import subprocess
from multiprocessing import Pool

DATASET_DIR = "dataset"

completed = 0
success = 0

def callback(result):
    global completed
    global success
    completed += 1
    success += result

def setup_and_run_simulation(input):
    directory, file = input
    tcl_file_contents = "log_wave -recursive *\nopen_vcd\nlog_vcd [get_object /testbench/inst*]\nrun all\nclose_vcd\nexit"
    # create tcl file called xsim_cfg.tcl if it doesn't exist
    try:
        with open(os.path.join(directory, "xsim_cfg.tcl"), "w") as f:
            f.write(tcl_file_contents)
        # put all verilog files in a list
        verilog_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".v"):
                verilog_files.append(filename)
    except:
        return 0
    # run xvlog on all verilog files
    try:
        subprocess.run(["xvlog"] + verilog_files, shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, cwd=directory)
    except subprocess.CalledProcessError as e:
        with open(os.path.join(directory, "compile_error.txt"), "w") as f:
            f.write("Error running xvlog")
            f.write("Used arguments: {}".format(["xvlog"] + verilog_files))
        return 0
    try:
        subprocess.run(["xelab", "-debug", "typical", "-top", "testbench", "-snapshot", "snapshot"], shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, cwd=directory)
    except subprocess.CalledProcessError as e:
        with open(os.path.join(directory, "compile_error.txt"), "w") as f:
            f.write("Error running xelab")
            f.write("Used arguments: {}".format(["xelab", "-debug", "typical", "-top", "testbench", "-snapshot", "snapshot"]))
        return 0
    try:
        subprocess.run(["xsim", "snapshot", "-tclbatch", "xsim_cfg.tcl"], shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, cwd=directory)
    except:
        with open(os.path.join(directory, "compile_error.txt"), "w") as f:
            f.write("Error running xsim")
            f.write("Used arguments: {}".format(["xsim", "snapshot", "-tclbatch", "xsim_cfg.tcl"]))
        return 0
    return 1


def setup_and_run_simulations():
    global completed
    global success
    completed = 0
    success = 0
    pool = Pool(processes=os.cpu_count()-2)
    create_sim_file_tasks = [] # list of tuples containing (directory, filename)
    folder_count = 0
    # loop through folders in DATASET
    for folder in os.listdir(DATASET_DIR):
        folder_count += 1
        # skip if folder does not contains a file ending with tb.v
        if not any(filename.endswith("tb.v") for filename in os.listdir(os.path.join(DATASET_DIR, folder))) or any(filename.endswith("error.txt") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
            # print("skipping {}".format(folder))
            continue
        file = ""
        
        for filename in os.listdir(os.path.join(DATASET_DIR, folder)):
            if filename.endswith(".v") and not filename.endswith("tb.v"):
                file = filename
                break
        create_sim_file_tasks.append((os.path.join(DATASET_DIR, folder), file))

    print("Set up simulation file tasks")
    total_tasks = len(create_sim_file_tasks)
    print("Going through {} of {} folders".format(total_tasks, folder_count))
    for task in create_sim_file_tasks:
        pool.apply_async(setup_and_run_simulation, args=(task,), callback=callback)
    while total_tasks > completed:
        print("Number of tasks left: {}".format(total_tasks - completed))
        time.sleep(20)
    pool.close()
    pool.join()
    try:
        print("Number of successful simulations: {}".format(success))
    except:
        pass
    print("Finished creating waveforms")
    pool.terminate()


if __name__ == "__main__":
    setup_and_run_simulations()