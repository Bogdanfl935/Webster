class ErrorHandler:
    def __init__(self, timestamp, status, error, message, path):
        self.timestamp = timestamp
        self.status = status
        self.error = error
        self.message = message
        self.path = path