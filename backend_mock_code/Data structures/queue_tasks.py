
#Jeremiah
class TodoQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, task):
        self.queue.append(task)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def size(self):
        return len(self.queue)

    def peek(self):
        return self.queue[0] if self.queue else None
