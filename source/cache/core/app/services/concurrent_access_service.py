from app.constants.lock_types import LockType

def acquire_lock(lock_type: LockType):
    lock_type.lock.acquire()

def release_lock(lock_type: LockType):
    lock_type.lock.release()


