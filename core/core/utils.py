from .models import Task

def round_robin_prioritization(tasks):
    update_tasks = tasks.order_by('estimated_time')

    prioritized_tasks = list(update_tasks)
    return prioritized_tasks
