import time
import sys
import os
sys.path.append(os.path.abspath('.'))
from concurrent_processor import retry_with_backoff

class MockAPI:
    def __init__(self):
        self.calls = 0

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=1.0)
    def failing_call(self):
        self.calls += 1
        print(f"Call attempt {self.calls}")
        if self.calls < 3:
            raise ValueError("Simulated 500 Internal Server Error")
        return "Success on try 3"

def main():
    api = MockAPI()
    start = time.time()
    try:
        result = api.failing_call()
        end = time.time()
        print(f"Result: {result} | Total calls: {api.calls} | Total time: {end - start:.2f}s")
    except Exception as e:
        print(f"Failed completely: {e}")

if __name__ == "__main__":
    main()
