import time
import random
import json
import subprocess
from multiprocessing import Pool
import os

'''
 Goes through the existing dataset and adds optional additional waveforms to it.
'''

DATASET_DIR = "../dataset"

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

    timer_file = os.path.join(directory, "timer.json")
    timer_file1 = os.path.join(directory, "timer1.json")
    timer_file2 = os.path.join(directory, "timer2.json")
    timer_file3 = os.path.join(directory, "timer3.json")
    diag_file1 = os.path.join(directory, "optional_timingdiagram1.png")
    diag_file2 = os.path.join(directory, "optional_timingdiagram2.png")
    diag_file3 = os.path.join(directory, "optional_timingdiagram3.png")

    try:
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
                    data["config"] = {}
                    data["config"]["hscale"] = 3

        if len(data["signal"]) >= 4:
            try:
                subset = data["signal"][2:] # first two signals are often clock and reset, try to keep those where they are
                random.shuffle(subset)
                optional_d1 = subset
                if (len(data["signal"]) > 4):
                    random.shuffle(subset)
                    optional_d2 = subset
                    random.shuffle(subset)
                    optional_d3 = subset
                # write the shuffled data to timer1.json, timer2.json, and timer3.json
                with open(timer_file1, 'w') as f:
                    json.dump({"signal": data["signal"][:2] + optional_d1, "config": data["config"]}, f, indent=4)
                if (len(data["signal"]) > 4):
                    with open(timer_file2, 'w') as f:
                        json.dump({"signal": data["signal"][:2] + optional_d2, "config": data["config"]}, f, indent=4)
                    with open(timer_file3, 'w') as f:
                        json.dump({"signal": data["signal"][:2] + optional_d3, "config": data["config"]}, f, indent=4)
                additional_waveforms = True
            except Exception as e:
                print(1, e)
                return 0

        if additional_waveforms:
            try:
                subprocess.run(["wavedrom-cli", "-i", timer_file1, "-p", diag_file1], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
                if (len(data["signal"]) > 4):
                    subprocess.run(["wavedrom-cli", "-i", timer_file2, "-p", diag_file2], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
                    subprocess.run(["wavedrom-cli", "-i", timer_file3, "-p", diag_file3], shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=True)
            except Exception as e:
                print(2, e)
                return 0
        return 1
    except:
        return 0


def create_waveforms():
    global completed
    global success
    completed = 0
    success = 0
    pool = Pool(processes=os.cpu_count()-2)
    create_sim_file_tasks = [] # list of tuples containing (directory, filename)
    # loop through folders in DATASET
    for folder in os.listdir(DATASET_DIR):
        # skip if folder does not contain a timer.json file
        if not any(filename.endswith("timer.json") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
            continue
        # skip if folder already contains a timer1.json file indicating it already has optional waveforms
        if any(filename.endswith("timer1.json") for filename in os.listdir(os.path.join(DATASET_DIR, folder))):
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
    print("Done")
    exit(0)