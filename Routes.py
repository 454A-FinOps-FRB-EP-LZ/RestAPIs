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

# GET request for creating a CPU load at 25%, 50% or 75%

@api.route('/stress/cpu', methods=['GET'])
def stress_cpu():
    cpu_load_percentage = random.choice([25, 50, 75])
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=cpu_stress, args=(cpu_load_percentage,))
        processes.append(process)
        process.start()
    return jsonify({'status': f'CPU stress test started at {cpu_load_percentage}% load'}), 200

# GET request for creating a memory load at 25%, 50% or 75%

@api.route('/stress/memory', methods=['GET'])
def stress_memory():
    # Getting the total memory in bytes
    total_memory = os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
    memory_load_percentage = random.choice([25, 50, 75])
    memory_to_allocate = int(total_memory*memory_load_percentage/100.0)
    try:
        memory_hog = bytearray(memory_to_allocate)
    except MemoryError:
        return jsonify({'status': 'Memory limit reached'}), 200
    return jsonify({'status': f'Memory stress test started at {memory_load_percentage}% load', 'memory_allocated': len(memory_hog)}), 200

# Running the API
# change host for public addr?
api.run(host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
