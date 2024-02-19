import time
import os
import subprocess
import json
from multiprocessing import Pool
import hdlparse.verilog_parser as vlog

DATASET_DIR = "dataset"

completed = 0
success = 0

def callback(result):
    global completed
    global success
    completed += 1
    success += result


def try_gentbvlog(inputfile, top, outputfile, clks, rsts):
    try:
        subprocess_args = ["gentbvlog",
                            "-in", inputfile,
                            "-top", top, 
                            "-out", outputfile
        ]
        # for every clk add -'clk' 'clk' to subprocess_args
        for clk in clks:
            subprocess_args.extend(["-clk", clk])
        # for every rst add -'rst' 'rst' to subprocess_args
        for rst in rsts:
            subprocess_args.extend(["-rst", rst])
        subprocess.run(subprocess_args, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        # write error to error.txt
        with open(os.path.join(os.path.dirname(inputfile), "gentbvlog_error.txt"), "w") as f:
            f.write("Error creating testbench file using gentbvlog")
            f.write("Used arguments: {}".format(subprocess_args))
        return False
    # check if testbench file was created
    if not os.path.exists(outputfile):
        # write error to error.txt
        with open(os.path.join(os.path.dirname(inputfile), "gentbvlog_error.txt"), "w") as f:
            f.write("Error creating testbench file using gentbvlog")
            f.write("Used arguments: {}".format(subprocess_args))
        return False
    return True


def try_testbench_generator(inputfile):
    try:
        subprocess.run(["python3", "testbench_generator.py", "-f", inputfile], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # check if testbench file was created
        if not os.path.exists(os.path.join(os.path.dirname(inputfile), "{}_tb.v".format(os.path.splitext(os.path.basename(inputfile))[0]))):
            # write error to error.txt
            with open(os.path.join(os.path.dirname(inputfile), "testbench_generator_error.txt"), "w") as f:
                f.write("Error creating testbench file using testbench-generator")
                f.write("Used arguments: {}".format(["python3", "testbench-generator", "-f", inputfile]))
            return False
    except:
        with open(os.path.join(os.path.dirname(inputfile), "testbench_generator_error.txt"), "w") as f:
            f.write("Error creating testbench file using testbench-generator")
            f.write("Used arguments: {}".format(["python3", "testbench-generator", "-f", inputfile]))
        return False
    return True


def try_tbgen(inputfile):
    try:
        subprocess.run(["python3", "tbgen", inputfile, os.path.join(os.path.dirnmae(inputfile), "{}_tb.v".format(os.path.splitext(os.path.basename(inputfile))[0]))], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # check if testbench file was created
        if not os.path.exists(os.path.join(os.path.dirname(inputfile), "{}_tb.v".format(os.path.splitext(os.path.basename(inputfile))[0]))):
            # write error to error.txt
            with open(os.path.join(os.path.dirname(inputfile), "tbgen_error.txt"), "w") as f:
                f.write("Error creating testbench file using tbgen")
                f.write("Used arguments: {}".format(["python3", "tbgen", inputfile, os.path.join(os.path.dirnmae(inputfile), "{}_tb.v".format(os.path.splitext(os.path.basename(inputfile))[0]))]))
            return False
    except:
        with open(os.path.join(os.path.dirname(inputfile), "tbgen_error.txt"), "w") as f:
            f.write("Error creating testbench file using tbgen")
            f.write("Used arguments: {}".format(["python3", "tbgen", inputfile, os.path.join(os.path.dirnmae(inputfile), "{}_tb.v".format(os.path.splitext(os.path.basename(inputfile))[0]))]))
        return False
    return True


def create_testbench(arg):
    directory, filename = arg
    vlog_ex = vlog.VerilogExtractor()
    # if the file is a verilog file
    if filename.endswith(".v"):
        try:
            # try:
            #     # subprocess.run(["verilog-format.exe", "-f", os.path.join(directory, filename)])
            # except:
            #     pass
            try:
                vlog_mods = vlog_ex.extract_objects(os.path.join(directory, filename))
            except Exception as e:
                print("Error reading verilog file")
                print(e)
                return 0

            ports = []
            mod_name = ""
            for mod in vlog_mods:
                if mod.name == os.path.splitext(filename)[0]:
                    ports = mod.ports
                    mod_name = mod.name
                    break

            clock_names = []
            reset_names = []
            input_port_names = []
            output_port_names = []
            possible_clock_names = ["clk", "clock"]
            possible_reset_names = ["rst", "reset", "nreset", "n_reset", "rst_n", "reset_n", "n_rst"]
            not_clock_names = ["clk_en", "clk_ena", "clk_enable", "clk_enable_n", "clk_en_n", "clk_en_n", "clk_ena", "clk_rst", "clk_rst_n", "clk_reset", "clk_reset_n", "clk_rst"]
            for port in ports:
                if port.mode == "input":
                    input_port_names.append(port.name)
                    if any(name in port.name for name in possible_clock_names) and not any(name in port.name for name in not_clock_names):
                        clock_names.append(port.name)
                    if any(name in port.name for name in possible_reset_names):
                        reset_names.append(port.name)
                elif port.mode == "output":
                    output_port_names.append(port.name)

            port_names = input_port_names + output_port_names

            succ = try_gentbvlog(os.path.join(directory, filename), mod_name, os.path.join(directory, "{}_tb.v".format(os.path.splitext(filename)[0])), clock_names, reset_names)
            # if not succ:
            #     succ = try_tbgen(os.path.join(directory, filename))
            if not succ:
                succ = try_testbench_generator(os.path.join(directory, filename))
            if not succ:
                return 0

        except:
            with open(os.path.join(directory, "error.txt"), "w") as f:
                f.write("Error reading verilog file")
            return 0    
        try:
            port_paths = {'paths': []}
            for p in port_names:
                port_paths['paths'].append("testbench/inst/{}".format(p))
            # write port paths to json file
            with open(os.path.join(directory, "port_paths.json"), "w") as f:
                json.dump(port_paths, f)
        except:
            with open(os.path.join(directory, "error.txt"), "w") as f:
                f.write("Error creating testbench file")
            return 0
    return 1

def create_testbenches():
    global completed
    global success
    process_pool = Pool(processes=os.cpu_count()-6)
    # can_start = False
    tasks = [] # list of tuples containing (directory, filename)
    total_tasks = 0
    total_folders = len(os.listdir(DATASET_DIR))

    # loop through folders in DATASET
    for folder in os.listdir(DATASET_DIR):
        # skip if folder contnains a file ending with tb.v or error.txt
        # if any(filename.endswith("tb.v") or filename.endswith("error.txt") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
        #     continue
        if any(filename.endswith("tb.v") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
            continue
        # skip if folder contains a file ending with tb.sv, this means testbench has already been generated for this file
        # if any(filename.endswith("tb.v") or filename.endswith("error.txt") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
        #     continue
        # read the verilog file in the folder
        for filename in os.listdir(os.path.join(DATASET_DIR, folder)):
            # if the file is a verilog file
            if filename.endswith(".v"):
                tasks.append((os.path.join(DATASET_DIR, folder), filename))

    total_tasks = len(tasks)
    print("Going through {} of {} folders".format(total_tasks, total_folders))
    for task in tasks:
        process_pool.apply_async(create_testbench, args=(task,), callback=callback)

    while total_tasks > completed:
        print("Tasks {} completed out of {}".format(completed, total_tasks))
        time.sleep(30)
    process_pool.close()
    process_pool.join()
    try:
        print("Number of successful setups: {}".format(sum(success)))
    except:
        pass
    print("Finished setting up testbenches files")
    process_pool.terminate()



if __name__ == "__main__":
    create_testbenches()