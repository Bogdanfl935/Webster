from enum import Enum, auto
import threading

class LockType(Enum):
    def __init__(self, *args, **kwargs):
        self.lock = threading.Lock()
    
    CRAWLER_STATUS_LOCK = auto()
    CRAWLER_CONTINUATION_LOCK = auto()
    LAST_URL_LOCK = auto()
    LAST_PARSED_LOCK = auto()