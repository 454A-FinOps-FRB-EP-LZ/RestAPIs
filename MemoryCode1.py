import psutil
import logging
import time
import sys
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class MemoryStressTester:
    def __init__(self, percentage):
        if not (0 < percentage <= 100):
            raise ValueError("Percentage must be between 1 and 100.")
        self.percentage = percentage
        self.memory_block = None
    def allocate_memory(self):
        """
        Allocates memory equal to the specified percentage of the total system memory.
        """
        total_memory = psutil.virtual_memory().total
        memory_to_consume = int(total_memory * (self.percentage / 100))
        logging.info(f"Allocating {memory_to_consume / (1024**2):.2f} MB of memory ({self.percentage}%).")
        try:
            # Allocate memory
            self.memory_block = bytearray(memory_to_consume)
            logging.info("Memory allocation successful.")
        except MemoryError:
            logging.error("Failed to allocate the requested memory.")
            sys.exit(1)
    def release_memory(self):
        """
        Releases the allocated memory.
        """
        self.memory_block = None
        logging.info("Memory has been released.")
if __name__ == "__main__":
    # Set the memory percentage to consume
    memory_percentage = 30  # Adjust this value as needed
    stress_tester = MemoryStressTester(memory_percentage)
    try:
        stress_tester.allocate_memory()
        logging.info("Press Ctrl+C to release memory and exit.")
        while True:
            time.sleep(1)  # Keeps the memory allocated until interrupted
    except KeyboardInterrupt:
        logging.info("Exiting due to user interrupt.")
    finally:
        stress_tester.release_memory()
