from pyqccapi.task.api_task import Task
from pyqccapi.task.task_invoker import ApiInvoker
from pyqccapi.environment import *
import os

path_config_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
path_config_file = os.path.join(path_config_dir,'config.yaml')

Environment(path_config_file)


def to_task_invoker(task: Task):
    return ApiInvoker(task)
