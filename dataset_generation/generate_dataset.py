import time
import os
import re
import threading
import multiprocessing
from datasets import load_dataset
from multiprocessing import Pool
import hdlparse.verilog_parser as vlog
import concurrent.futures

DATASET_DIR = "../dataset"

main_working_dir = os.getcwd()

completed = 0
success = 0

def callback(result):
    global completed
    global success
    completed += 1
    success += result


def create_dataset_folder(id, module_name, content):
    try:
        # delete folder if it already exists
        if os.path.exists(os.path.join(DATASET_DIR, "ds_{}".format(id))):
            os.rmdir(os.path.join(DATASET_DIR, "ds_{}".format(id)))
        os.mkdir(os.path.join(DATASET_DIR, "ds_{}".format(id)))
        with open(os.path.join(DATASET_DIR, "ds_{}".format(id), "{}.v".format(module_name)), "w", encoding="utf-8") as f:
            f.write(content)
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
    futures = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)
    extractor = vlog.VerilogExtractor()
    counter = 0
    total = len(ds['train'])
    for data in ds['train']:
        verilog_modules = extractor.extract_objects_from_source(data['module_content'])
        # retrieve module name from data['module_content']
        # check if module folder already exists
        for m in verilog_modules:
            module_name = m.name
            futures.append(executor.submit(create_dataset_folder, counter, module_name, data['module_content']))
        counter += 1
        if counter % 1000 == 0:
            print("Processed {} of {} modules".format(counter, total))
    for future in futures:
        future.result()
if __name__ == "__main__":
    create_dataset()