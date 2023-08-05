from pyqccapi.task.api_task import Task
from pyqccapi.task.task_invoker import ApiInvoker
from pyqccapi.environment import *

Environment('../config.yaml')


def to_task_invoker(task: Task):
    return ApiInvoker(task)
