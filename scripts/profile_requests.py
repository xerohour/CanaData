import requests
import time
from concurrent.futures import ThreadPoolExecutor

def test_session_vs_requests():
    url = "https://httpbin.org/get"

    # Using requests.get
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(requests.get, url) for _ in range(50)]
        for f in futures:
            f.result()
    end_req = time.time() - start

    # Using Session
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
    session.mount('https://', adapter)

    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(session.get, url) for _ in range(50)]
        for f in futures:
            f.result()
    end_sess = time.time() - start

    print(f"requests.get: {end_req:.2f}s")
    print(f"session.get: {end_sess:.2f}s")

if __name__ == '__main__':
    test_session_vs_requests()
