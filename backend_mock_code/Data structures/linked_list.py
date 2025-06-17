
#Amani and Ray (Linked List Implementation)

class TodoLinkedList:
    """
    Linked List implementation for storing todo tasks
    Provides O(1) insertion at head and O(n) search/deletion
    """
    def __init__(self):
        self.head = None        # Points to first node
        self.size = 0          # Track number of nodes
        self.next_id = 1       # Auto-increment ID counter

    def add_task(self, title, description, priority="medium"):
        """
        Add new task to the beginning of linked list (O(1) operation)
        """
        # Create new node with auto-incremented ID
        new_node = TodoNode(self.next_id, title, description, priority)
        
        # Insert at head of linked list
        new_node.next = self.head
        self.head = new_node
        
        # Update counters
        self.next_id += 1
        self.size += 1
        
        return new_node.to_dict()

    def get_all_tasks(self):
        """
        Traverse entire linked list and return all tasks as array
        Time complexity: O(n)
        """
        tasks = []
        current = self.head
        
        # Traverse from head to tail
        while current:
            tasks.append(current.to_dict())
            current = current.next
            
        return tasks

    def find_task(self, task_id):
        """
        Search for task by ID in linked list
        Time complexity: O(n)
        """
        current = self.head
        
        # Linear search through linked list
        while current:
            if current.task_id == task_id:
                return current
            current = current.next
            
        return None

    def update_task(self, task_id, title=None, description=None, priority=None, completed=None):
        """
        Update existing task properties
        Time complexity: O(n) for search + O(1) for update
        """
        task_node = self.find_task(task_id)
        
        if not task_node:
            return None
            
        # Update only provided fields
        if title is not None:
            task_node.title = title
        if description is not None:
            task_node.description = description
        if priority is not None:
            task_node.priority = priority
        if completed is not None:
            task_node.completed = completed
            
        return task_node.to_dict()

    def delete_task(self, task_id):
        """
        Delete task from linked list
        Time complexity: O(n)
        """
        # Handle empty list
        if not self.head:
            return False
            
        # Handle deletion of head node
        if self.head.task_id == task_id:
            self.head = self.head.next
            self.size -= 1
            return True
            
        # Search for node to delete
        current = self.head
        while current.next:
            if current.next.task_id == task_id:
                # Remove node by updating pointer
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
            
        return False