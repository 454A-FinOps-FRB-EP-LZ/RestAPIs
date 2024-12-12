from flask import Flask, request, jsonify
import psutil
import logging
import threading
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
memory_block = None
lock = threading.Lock()
def allocate_memory(percentage):
    """
    Allocates memory equal to the specified percentage of the total system memory.
    """
    global memory_block
    if not (0 < percentage <= 100):
        raise ValueError("Percentage must be between 1 and 100.")
    with lock:
        total_memory = psutil.virtual_memory().total
        memory_to_consume = int(total_memory * (percentage / 100))
        logging.info(f"Allocating {memory_to_consume / (1024 ** 2):.2f} MB of memory ({percentage}%).")
        try:
            # Allocate memory
            memory_block = bytearray(memory_to_consume)
            logging.info("Memory allocation successful.")
        except MemoryError:
            logging.error("Failed to allocate the requested memory.")
            raise
def release_memory():
    """
    Releases the allocated memory.
    """
    global memory_block
    with lock:
        memory_block = None
        logging.info("Memory has been released.")
@app.route('/consume_memory', methods=['POST'])
def consume_memory():
    """
    API endpoint to consume memory.
    """
    try:
        data = request.get_json()
        percentage = data.get('percentage', 0)
        if not (0 < percentage <= 100):
            return jsonify({'error': 'Percentage must be between 1 and 100.'}), 400
        allocate_memory(percentage)
        return jsonify({'status': f'{percentage}% memory allocated successfully.'}), 200
    except MemoryError:
        return jsonify({'error': 'Memory allocation failed. Insufficient resources.'}), 500
    except Exception as e:
        logging.exception("Error in /consume_memory")
        return jsonify({'error': str(e)}), 500
@app.route('/release_memory', methods=['POST'])
def free_memory():
    """
    API endpoint to release allocated memory.
    """
    try:
        release_memory()
        return jsonify({'status': 'Memory has been released.'}), 200
    except Exception as e:
        logging.exception("Error in /release_memory")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
