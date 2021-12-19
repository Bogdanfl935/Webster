from enum import Enum, auto
import threading

class LockType(Enum):
    def __init__(self, *args, **kwargs):
        self.lock = threading.Lock()
    
    STATUS_LOCK = auto()
    CONTINUATION_LOCK = auto()