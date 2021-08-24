# Global vars
"""
# MC Projects
mc_projects = [
    ["44073", "Team Passerelles"],
    ["44076", "Mobile"],
    ["47266", "RS&DE - Data Science"]
]
"""
# Max Projects
max_projects = [
    ["57605", "Team Passerelles"],
    ["57606", "Mobile"],
    ["57608", "RS&DE - Data Science"]
]
# Generic Projects
generic_projects = [
    ["44075", "Team DevOps"],
    ["44077", "Kronos IA"],
    ["55311", "Security Awareness Program"]
]

tasks_array = max_projects + generic_projects


def get_default_task():
    return tasks_array[0][0]


def get_tasks_ids():
    return [task[0] for task in tasks_array]


def get_tasks_values():
    return [task[1] for task in tasks_array]


def is_valid_task_id(task_id):
    valid_task_ids = get_tasks_ids()
    if task_id in valid_task_ids:
        return True
    return False


def get_task_index_by_id(task_id):
    indexes = [(ix, iy) for ix, row in enumerate(tasks_array) for iy, i in enumerate(row) if i == task_id]
    if indexes:
        return indexes[0][0]
    return 0


def get_task_id_by_index(index):
    if index < 0 | index > len(tasks_array):
        return ""
    return tasks_array[index][0]
