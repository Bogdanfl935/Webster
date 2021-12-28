import threading

__lock_cache = dict()

def acquire_user_lock(user_id: int):
    lock = __lock_cache.get(user_id, None)
    
    if lock is None:
        lock = threading.Lock()
        __lock_cache[user_id] = lock

    lock.acquire()

def release_user_lock(user_id: int):
    lock = __lock_cache.pop(user_id, None)
    
    if lock is not None:
        lock.release()