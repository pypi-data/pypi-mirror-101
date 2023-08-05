from pyqccapi.base.api_config import ApiConfig

import uuid


class Task:
    """
    一个实体类，包含一个任务需要的全部信息
    """

    def __init__(self, method, params):
        self.method = method
        self.params = params
        self.success = False
        self.code = ''
        self.message = ''
        self.data = None

    def to_method_detail(self):
        return ApiConfig.to_instance().to_method_detail(self.method)

    def to_request_url(self):
        return self.to_method_detail()['Titles']['paramList']['apiUrl']


class AsyncTask(Task):
    """
    异步任务，所以它需要一个id
    因为懒，使用uuid4
    正确的做法：
    分布式环境下：机器名+时间戳+自增序列
    单机环境下：md5(mac/机器名+时间戳+自增序列+salt)
    """

    def __init__(self, method, params):
        Task.__init__(self, method, params)
        self.task_id = uuid.uuid4().hex





