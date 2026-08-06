import time


def run_basic_benchmark():
    start = time.time()
    # Simple benchmark to make sure things are working
    print("Running basic benchmark")
    time.sleep(1)
    end = time.time()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    run_basic_benchmark()
