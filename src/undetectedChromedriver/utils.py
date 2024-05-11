import time
import random
from tqdm import tqdm


def random_sleep_with_progress(total_seconds):
    sleep_time = random.uniform(0.7, 1.3) * total_seconds
    sleep_time = max(sleep_time, 0.0)
    print(" - INFO - Sleep_time: ", sleep_time)
    for _ in tqdm(range(int(sleep_time * 10)), desc="Sleeping", unit="milliseconds"):
        time.sleep(0.1)
    print(f" - INFO - Sleep completed: {sleep_time:.2f} seconds")