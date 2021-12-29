from concurrent.futures import ThreadPoolExecutor, Future
import threading, queue

__lock_cache = dict()
__futures_queue = queue.Queue()
__executor = ThreadPoolExecutor()

class __StopCondition():
    def __init__(self):
        pass


def acquire_user_lock(authenticated_user: str):
    lock = __lock_cache.get(authenticated_user, None)
    
    if lock is None:
        lock = threading.Lock()
        __lock_cache[authenticated_user] = lock

    lock.acquire()

def release_user_lock(authenticated_user: str):
    lock = __lock_cache.pop(authenticated_user, None)
    
    if lock is not None:
        lock.release()


def submit_task(task):
    __futures_queue.put(__executor.submit(task), block=False)

def shutdown():
     __futures_queue.put(__StopCondition(), block=False)
        
def __await_futures():
    while True:
        content = __futures_queue.get(block=True)
        if isinstance(content, Future):
            content.result() # Consume future => Do not supress errors (if any)
        elif isinstance(content, __StopCondition):
            break
    
__executor_future_solver = threading.Thread(target=__await_futures, daemon=True)
__executor_future_solver.start()

