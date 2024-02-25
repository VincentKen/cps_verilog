import time
import os
import subprocess
import re

import threading
import multiprocessing
import random
import math
import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

DATASET_DIR = "dataset"

main_working_dir = os.getcwd()

completed = 0
success = 0

def callback(result):
    global completed
    global success
    completed += 1
    success += result
    
        
def generate_waveform(input):
    directory = input

    dump_file = os.path.join(directory, "dump.vcd")
    timer_file = os.path.join(directory, "timer.json")
    timer_file1 = os.path.join(directory, "timer1.json")
    timer_file2 = os.path.join(directory, "timer2.json")
    timer_file3 = os.path.join(directory, "timer3.json")
    diag_file = os.path.join(directory, "timingdiagram.png")
    
    try:
        subprocess.run(["python3", "-m", "vcd2wavedrom.vcd2wavedrom", "-i", dump_file, "-o", timer_file], shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        data = {}
        additional_waveforms = False
        has_large_data_fields = False
        # open timer.json
        with open(timer_file, 'r') as f:
            data = json.load(f)
            # loop through signals in data["signal"]
            for signal in data["signal"]:
                # remove 'testbench.inst' from signal["name"]
                signal["name"] = signal["name"].replace('testbench.inst.', '')
                # if any signal['data'] is longer than 4, set has_large_data_fields to True
                if any(len(d) > 4 for d in signal["data"]):
                    has_large_data_fields = True
                    break

        # if has_large_data_fields is True, change data["config"]["hscale"] to 3
        if has_large_data_fields:
            try:
                data["config"]["hscale"] = 3
            except:
                try:
                    data["config"] = {"hscale": 3}
                except:
                    pass
        
        if len(data["signal"]) > 6:
            try:
                subset = data["signal"][2:] # first two signals are often clock and reset, try to keep those where they are
                optional_d1 = random.shuffle(subset)
                optional_d2 = random.shuffle(subset)
                optional_d3 = random.shuffle(subset)
                # write the shuffled data to timer1.json, timer2.json, and timer3.json
                with open(timer_file1, 'w') as f:
                    json.dump({"signal": data["signal"][:2] + optional_d1, "config": data["config"]}, f, indent=4)
                with open(timer_file2, 'w') as f:
                    json.dump({"signal": data["signal"][:2] + optional_d2, "config": data["config"]}, f, indent=4)
                with open(timer_file3, 'w') as f:
                    json.dump({"signal": data["signal"][:2] + optional_d3, "config": data["config"]}, f, indent=4)
                additional_waveforms = True
            except:
                pass

        # write the new data to timer.json
        with open(timer_file, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        return 0
    # return 0
    try:
        subprocess.run(["wavedrom-cli", "-i", timer_file, "-p", diag_file], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
        if additional_waveforms:
            try:
                subprocess.run(["wavedrom-cli", "-i", timer_file1, "-p", diag_file.replace("timingdiagram", "optional_timingdiagram1")], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
                subprocess.run(["wavedrom-cli", "-i", timer_file2, "-p", diag_file.replace("timingdiagram", "optional_timingdiagram2")], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
                subprocess.run(["wavedrom-cli", "-i", timer_file3, "-p", diag_file.replace("timingdiagram", "optional_timingdiagram3")], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
            except:
                pass
    except:
        return 0
    return 1


def create_waveforms():
    global completed
    global success
    completed = 0
    success = 0
    pool = Pool(processes=os.cpu_count()-2)
    create_sim_file_tasks = [] # list of tuples containing (directory, filename)
    # loop through folders in DATASET
    for folder in os.listdir(DATASET_DIR):
        # skip if folder does not contains a file ending with tb.v
        if not any(filename.endswith("dump.vcd") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
            # print("skipping {}".format(folder))
            continue
        create_sim_file_tasks.append((os.path.join(DATASET_DIR, folder)))

    print("Set up waveform tasks")
    total_tasks = len(create_sim_file_tasks)
    for task in create_sim_file_tasks:
        pool.apply_async(generate_waveform, args=(task,), callback=callback)
    while total_tasks > completed:
        print("Number of tasks left: {}".format(total_tasks - completed))
        time.sleep(30)
    pool.close()
    pool.join()
    print("Number of successful waveforms: {}".format(success))
    print("Finished creating waveforms")
    pool.terminate()


if __name__ == "__main__":
    create_waveforms()