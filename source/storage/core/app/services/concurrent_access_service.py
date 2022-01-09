import threading

__lock_cache = dict()
__cache_access_lock = threading.Lock()

def acquire_user_lock(user_id: int):
    __cache_access_lock.acquire()
    lock = __lock_cache.get(user_id, None)
    
    if lock is None:
        lock = threading.Lock()
        __lock_cache[user_id] = lock
    __cache_access_lock.release()
    lock.acquire()

def release_user_lock(user_id: int):
    __cache_access_lock.acquire()
    lock = __lock_cache.pop(user_id, None)
    
    if lock is not None:
        lock.release()
    __cache_access_lock.release()