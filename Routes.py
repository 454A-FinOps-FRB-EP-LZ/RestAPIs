# https://blog.stoplight.io/python-rest-api
# cpu use multiprocessing & os
# multiprocessing: https://docs.python.org/3/library/multiprocessing.html

from flask import Flask, jsonify
import multiprocessing
import os
import random
import time
import psutil
import threading

# Defining the API

api = Flask(__name__)

# Function for creating a CPU load at the percentage passed as a parameter

def cpu_stress(percentage):
    start_time = time.time()
    while True:
        if time.time()-start_time > percentage/100.0:
            time.sleep(1-(percentage/100.0))
            start_time = time.time()

# Global variable for storing a memory load

memory_hog = None

# Thread lock for making thread-safe memory functions

lock = threading.Lock()

# Function for allocating memory loads

def memory_allocate(percentage):
    global memory_hog
    with lock:
        total_memory = psutil.virtual_memory().total
        memory_to_allocate = int(total_memory*percentage/100.0)
        try:
            memory_hog = bytearray(memory_to_allocate)
        except MemoryError:
            raise MemoryError('Memory limit reached')

# Function for freeing memory loads

def memory_free():
    global memory_hog
    with lock:
        memory_hog = None

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
    memory_load_percentage = random.choice([5, 10, 15, 20])
    try:
        memory_allocate(memory_load_percentage)
        timer = threading.Timer(3.0, memory_free)
        timer.start()
    except MemoryError:
        return jsonify({'status': 'Memory limit reached'}), 200
    return jsonify({'status': f'Memory stress test started at {memory_load_percentage}% load'}), 200

# Running the API

api.run(host="0.0.0.0", port=int(os.environ.get("PORT", 1313)))
