from concurrent.futures import ThreadPoolExecutor
import threading

__lock_cache = dict()

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
        

    

executor = ThreadPoolExecutor()