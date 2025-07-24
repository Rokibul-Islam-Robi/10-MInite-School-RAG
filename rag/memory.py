from collections import deque

class ShortTermMemory:
    def __init__(self, max_length=10):
        self.history = deque(maxlen=max_length)

    def add(self, user, message):
        self.history.append((user, message))

    def get_history(self):
        return list(self.history)

# Long-term memory is handled by the vector DB (see db.py) 