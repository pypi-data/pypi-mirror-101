import json
from pyqccapi.task.api_task import Task


class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return {
                'method': obj.method,
                'params': obj.params,
                'success': obj.success,
                'code': obj.code,
                'message': obj.message,
                'data': obj.data
            }
        return json.JSONEncoder.default(self, obj)
