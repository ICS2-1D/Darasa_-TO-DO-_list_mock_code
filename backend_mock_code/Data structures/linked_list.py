
# Amani and Ray (Linked List Implementation)

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class PrintJob:
    job_id: int
    user_id: str
    title: str
    priority: int = 5  # Lower number = higher urgency
    created_at: datetime = None


class PrintQueue(ABC):
    @abstractmethod
    def enqueue(self, job):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def snapshot(self):
        pass

    @abstractmethod
    def remove_expired_jobs(self, max_wait_seconds):
        pass


class LinkedListPrintQueue(PrintQueue):
    def __init__(self):
        self.head = None
        self.size = 0
        self.next_job_id = 1

    def enqueue(self, job):
        """
        Add new print job at head of linked list.
        Assigns auto-incremented job ID and creation timestamp.
        """
        job.job_id = self.next_job_id
        job.created_at = datetime.now()
        new_node = LinkedListNode(job)
        new_node.next = self.head
        self.head = new_node
        self.next_job_id += 1
        self.size += 1

    def dequeue(self):
        """
        Remove and return the highest-priority job (lowest priority number).
        For simplicity, we'll scan the list to find the minimum.
        """
        if not self.head:
            return None

        prev_min = None
        current_prev = None
        current = self.head
        min_node = self.head
        min_prev = None

        while current:
            if current.job.priority < min_node.job.priority:
                min_node = current
                min_prev = current_prev
            current_prev = current
            current = current.next

        if min_prev is None:
            # Min node is head
            self.head = self.head.next
        else:
            min_prev.next = min_node.next

        self.size -= 1
        return min_node.job

    def snapshot(self):
        """
        Return list of job dictionaries for visualization/logging.
        """
        result = []
        current = self.head
        while current:
            job = current.job
            result.append({
                'job_id': job.job_id,
                'user_id': job.user_id,
                'title': job.title,
                'priority': job.priority,
                'created_at': job.created_at.isoformat() if job.created_at else None
            })
            current = current.next
        return result

    def remove_expired_jobs(self, max_wait_seconds):
        """
        Remove jobs older than max_wait_seconds.
        """
        threshold = datetime.now() - timedelta(seconds=max_wait_seconds)
        current = self.head
        prev = None

        while current:
            if current.job.created_at < threshold:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
            else:
                prev = current
            current = current.next


class LinkedListNode:
    def __init__(self, job):
        self.job = job
        self.next = None