from threading import Thread
import time
import threading
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

class ThreadUtil:

    def task(self, n):
        print(f'SLEEPING: {threading.currentThread().getName()}: {n}')
        time.sleep(n / 10)
        print(f'DONE: {threading.currentThread().getName()}: {n}')
        return n / 10

if __name__ == '__main__':

    ex = futures.ThreadPoolExecutor(max_workers=10)
    results = ex.map(ThreadUtil().task, [10,10,10,10,10])
    real_results = list(results)
    print('main: results: {}'.format(real_results))