import time
import os
import re
import threading
import multiprocessing
from datasets import load_dataset
from multiprocessing import Pool
import hdlparse.verilog_parser as vlog

DATASET_DIR = "dataset"

main_working_dir = os.getcwd()

completed = 0
success = 0

def callback(result):
    global completed
    global success
    completed += 1
    success += result


def create_dataset_folder(args):
    module_name, module_content = args
    try:
        os.mkdir(os.path.join(DATASET_DIR, module_name))
        with open(os.path.join(DATASET_DIR, module_name, "{}.v".format(module_name)), "w", encoding="utf-8") as f:
            f.write(module_content)
        return 1
    except:
        return 0


def create_dataset():
    # create dataset directory if it doesn't exist
    if not os.path.exists(DATASET_DIR):
        os.mkdir(DATASET_DIR)
    global completed
    global success
    ds = load_dataset("wangxinze/Verilog_data")
    tasks = []
    pool = Pool(processes=os.cpu_count()-2)
    extractor = vlog.VerilogExtractor()
    counter = 0
    total = len(ds['train'])
    for data in ds['train']:
        verilog_modules = extractor.extract_objects_from_source(data['module_content'])
        # retrieve module name from data['module_content']
        # check if module folder already exists
        for m in verilog_modules:
            module_name = m.name
            if os.path.exists(os.path.join(DATASET_DIR, module_name)):
                continue

            try:
                os.mkdir(os.path.join(DATASET_DIR, module_name))
                # create verilog file with module name
                with open(os.path.join(DATASET_DIR, module_name, "{}.v".format(module_name)), "w", encoding="utf-8") as f:
                    f.write(data['module_content'])
            except:
                print("Error creating folder or writing verilog file")
        counter += 1
        if counter % 1000 == 0:
            print("Processed {} of {} modules".format(counter, total))
    # for task in tasks:
    #     pool.apply_async(create_dataset_folder, args=(task,), callback=callback)
    # while len(tasks) > completed:
    #     print("Tasks {} completed out of {}".format(completed, len(tasks)))
    #     time.sleep(20)
    # pool.close()
    # pool.join()
    # try:
    #     print("Number of successful dataset creations: {}".format(success))
    # except:
    #     pass

if __name__ == "__main__":
    create_dataset()