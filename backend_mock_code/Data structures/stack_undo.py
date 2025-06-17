
#Jolene (Stack Undo)

class TodoStack:
    def __init__(self, max_size=10):
        self.stack = []
        self.max_size = max_size

    def push(self, operation):
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)
        self.stack.append(operation)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def get_all(self):
        return self.stack.copy()
