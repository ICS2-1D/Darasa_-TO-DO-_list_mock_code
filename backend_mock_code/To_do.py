
# todo_backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

# Initialize Flask application
app = Flask(__name__)
# Enable CORS to allow frontend to communicate with backend
CORS(app)

# =====================================================
# DATA STRUCTURES IMPLEMENTATION
# =====================================================

class TodoNode:
    """
    Node class for implementing linked list structure
    Each node contains task data and pointer to next node
    """
    def __init__(self, task_id, title, description, priority="medium", completed=False):
        self.task_id = task_id          # Unique identifier for the task
        self.title = title              # Task title
        self.description = description  # Task description
        self.priority = priority        # Priority level (low, medium, high)
        self.completed = completed      # Completion status
        self.created_at = datetime.now().isoformat()  # Timestamp
        self.next = None               # Pointer to next node in linked list

    def to_dict(self):
        """Convert node data to dictionary for JSON serialization"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at
        }

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

class TodoStack:
    """
    Stack implementation for undo operations
    LIFO (Last In, First Out) data structure
    """
    def __init__(self, max_size=10):
        self.stack = []                 # Array-based stack
        self.max_size = max_size       # Limit stack size to prevent memory issues

    def push(self, operation):
        """
        Add operation to top of stack
        Time complexity: O(1)
        """
        # Remove oldest operation if stack is full
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)  # Remove from bottom
            
        # Add new operation to top
        self.stack.append({
            'operation': operation,
            'timestamp': datetime.now().isoformat()
        })

    def pop(self):
        """
        Remove and return top operation from stack
        Time complexity: O(1)
        """
        if self.stack:
            return self.stack.pop()
        return None

    def is_empty(self):
        """Check if stack is empty"""
        return len(self.stack) == 0

    def get_history(self):
        """Return all operations in stack (for debugging)"""
        return self.stack.copy()

class TodoQueue:
    """
    Queue implementation for task processing
    FIFO (First In, First Out) data structure
    """
    def __init__(self):
        self.queue = []     # Array-based queue

    def enqueue(self, task):
        """
        Add task to rear of queue
        Time complexity: O(1)
        """
        self.queue.append(task)

    def dequeue(self):
        """
        Remove and return task from front of queue
        Time complexity: O(n) due to array shifting
        """
        if self.queue:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        """Check if queue is empty"""
        return len(self.queue) == 0

    def size(self):
        """Return number of items in queue"""
        return len(self.queue)

    def peek(self):
        """Return front item without removing it"""
        if self.queue:
            return self.queue[0]
        return None

# =====================================================
# GLOBAL DATA STRUCTURES INITIALIZATION
# =====================================================

# Initialize main data structures
todo_list = TodoLinkedList()        # Main storage using linked list
undo_stack = TodoStack()           # Undo operations using stack
processing_queue = TodoQueue()     # Task processing using queue

# =====================================================
# API ENDPOINTS (CRUD OPERATIONS)
# =====================================================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    READ operation - Get all tasks
    Returns tasks sorted by priority and completion status
    """
    try:
        # Get all tasks from linked list
        tasks = todo_list.get_all_tasks()
        
        # Sort tasks: incomplete first, then by priority
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        tasks.sort(key=lambda x: (x['completed'], priority_order.get(x['priority'], 2)))
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'total': len(tasks)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    CREATE operation - Add new task
    Adds task to linked list and logs operation to stack
    """
    try:
        # Extract data from request
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('title'):
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        # Create new task in linked list
        new_task = todo_list.add_task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium')
        )
        
        # Log operation to undo stack
        undo_stack.push({
            'type': 'create',
            'task_id': new_task['task_id'],
            'data': new_task
        })
        
        # Add to processing queue if high priority
        if new_task['priority'] == 'high':
            processing_queue.enqueue(new_task)
        
        return jsonify({
            'success': True,
            'task': new_task,
            'message': 'Task created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    UPDATE operation - Modify existing task
    Updates task in linked list and logs operation to stack
    """
    try:
        data = request.get_json()
        
        # Store original task data for undo
        original_task = todo_list.find_task(task_id)
        if not original_task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        original_data = original_task.to_dict()
        
        # Update task in linked list
        updated_task = todo_list.update_task(
            task_id=task_id,
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority'),
            completed=data.get('completed')
        )
        
        if not updated_task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        # Log operation to undo stack
        undo_stack.push({
            'type': 'update',
            'task_id': task_id,
            'original_data': original_data,
            'new_data': updated_task
        })
        
        return jsonify({
            'success': True,
            'task': updated_task,
            'message': 'Task updated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE operation - Remove task
    Deletes task from linked list and logs operation to stack
    """
    try:
        # Store task data for undo before deletion
        task_to_delete = todo_list.find_task(task_id)
        if not task_to_delete:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        task_data = task_to_delete.to_dict()
        
        # Delete task from linked list
        success = todo_list.delete_task(task_id)
        
        if success:
            # Log operation to undo stack
            undo_stack.push({
                'type': 'delete',
                'task_id': task_id,
                'data': task_data
            })
            
            return jsonify({
                'success': True,
                'message': 'Task deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete task'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/undo', methods=['POST'])
def undo_operation():
    """
    UNDO operation - Reverse last operation using stack
    Demonstrates stack (LIFO) data structure usage
    """
    try:
        # Pop last operation from stack
        last_operation = undo_stack.pop()
        
        if not last_operation:
            return jsonify({'success': False, 'error': 'No operations to undo'}), 400
        
        operation_data = last_operation['operation']
        
        # Reverse the operation based on type
        if operation_data['type'] == 'create':
            # Undo create by deleting the task
            todo_list.delete_task(operation_data['task_id'])
            message = f"Undid creation of task '{operation_data['data']['title']}'"
            
        elif operation_data['type'] == 'update':
            # Undo update by restoring original data
            original = operation_data['original_data']
            todo_list.update_task(
                task_id=original['task_id'],
                title=original['title'],
                description=original['description'],
                priority=original['priority'],
                completed=original['completed']
            )
            message = f"Undid update of task '{original['title']}'"
            
        elif operation_data['type'] == 'delete':
            # Undo delete by recreating the task
            task_data = operation_data['data']
            # Note: This is a simplified undo - in production, you'd need to restore exact position
            todo_list.add_task(
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data['priority']
            )
            message = f"Undid deletion of task '{task_data['title']}'"
        
        return jsonify({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/queue/process', methods=['POST'])
def process_next_task():
    """
    Process next task from queue
    Demonstrates queue (FIFO) data structure usage
    """
    try:
        # Dequeue next task from processing queue
        next_task = processing_queue.dequeue()
        
        if not next_task:
            return jsonify({'success': False, 'error': 'No tasks in processing queue'}), 400
        
        # Mark task as completed
        updated_task = todo_list.update_task(
            task_id=next_task['task_id'],
            completed=True
        )
        
        return jsonify({
            'success': True,
            'processed_task': updated_task,
            'message': f"Processed task: {next_task['title']}",
            'remaining_in_queue': processing_queue.size()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    Get application statistics
    Shows usage of different data structures
    """
    try:
        tasks = todo_list.get_all_tasks()
        
        # Calculate statistics using array operations
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t['completed']])
        pending_tasks = total_tasks - completed_tasks
        
        # Priority distribution
        priority_count = {'high': 0, 'medium': 0, 'low': 0}
        for task in tasks:
            priority_count[task['priority']] += 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'priority_distribution': priority_count,
                'undo_operations_available': len(undo_stack.stack),
                'tasks_in_processing_queue': processing_queue.size(),
                'linked_list_size': todo_list.size
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =====================================================
# APPLICATION STARTUP
# =====================================================

if __name__ == '__main__':
    # Add some sample data for testing
    print("Initializing To-Do List Backend...")
    print("Data Structures Used:")
    print("- Linked List: Main task storage")
    print("- Stack: Undo operations")
    print("- Queue: Task processing")
    print("- Arrays: Sorting and filtering")
    
    # Create sample tasks
    todo_list.add_task("Complete project documentation", "Write comprehensive docs", "high")
    todo_list.add_task("Review code", "Code review for pull request", "medium")
    todo_list.add_task("Update dependencies", "Upgrade to latest versions", "low")
    
    # Start Flask development server
    print("\nStarting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)