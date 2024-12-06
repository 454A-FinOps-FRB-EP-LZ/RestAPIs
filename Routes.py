# https://blog.stoplight.io/python-rest-api
# cpu use multiprocessing & os
# multiprocessing: https://docs.python.org/3/library/multiprocessing.html

from flask import Flask, jsonify
import multiprocessing
import os
import random
import time

# Defining the API

api = Flask(__name__)

# Function for creating a CPU load at the percentage passed as a parameter

def cpu_stress(percentage):
    start_time = time.time()
    while True:
        if time.time()-start_time > percentage/100.0:
            time.sleep(1-(percentage/100.0))
            start_time = time.time()

# Function for creating a memory load at the percentage passed as a parameter
 
def memory_stress(percentage, memory_hog):
    start_time = time.time()
    while time.time()-start_time > percentage/100.0:
        memory_hog.append(0)
        time.sleep(1-(percentage/100.0))
        start_time = time.time()

# GET request for creating a CPU load at 5%, 10%, 15 or 20%

@api.route('/stress/cpu', methods=['GET'])
def stress_cpu():
    cpu_load_percentage = random.choice([5, 10, 15, 20])
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=cpu_stress, args=(cpu_load_percentage,))
        processes.append(process)
        process.start()
    return jsonify({'status': f'CPU stress test started at {cpu_load_percentage}% load'}), 200

# GET request for creating a memory load at 5%, 10%, 15% or 20%

@api.route('/stress/memory', methods=['GET'])
def stress_memory():
    # Getting the total memory in bytes
    total_memory = os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
    memory_load_percentage = random.choice([5, 10, 15, 20])
    memory_to_allocate = int(total_memory*memory_load_percentage/100.0)
    try:
        memory_hog = bytearray(memory_to_allocate)
        time.sleep(3)
        del memory_hog
    except MemoryError:
        return jsonify({'status': 'Memory limit reached'}), 200
    return jsonify({'status': f'Memory stress test started at {memory_load_percentage}% load'}), 200

# Running the API

api.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
