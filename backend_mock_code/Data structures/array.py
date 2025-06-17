
#Davis(Arrays and Lists)

def sort_tasks(tasks):
    priority_order = {'high': 1, 'medium': 2, 'low': 3}
    return sorted(tasks, key=lambda x: (x['completed'], priority_order.get(x['priority'], 2)))

def calculate_stats(tasks):
    total = len(tasks)
    completed = len([t for t in tasks if t['completed']])
    pending = total - completed
    priority_count = {'high': 0, 'medium': 0, 'low': 0}
    for task in tasks:
        priority_count[task['priority']] += 1
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "priority_distribution": priority_count
    }
