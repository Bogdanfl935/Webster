from concurrent.futures import ThreadPoolExecutor, Future
import queue, threading

__futures_queue = queue.Queue()
__executor = ThreadPoolExecutor()

class __StopCondition():
    def __init__(self):
        pass

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