import hashlib
import time

import requests

from pyqccapi.constant import error_code
from pyqccapi.environment import Environment
from pyqccapi.task.api_task import *
from pyqccapi.util.yamls import *

encode = 'utf-8'
url_base = 'http://api.qichacha.com/'


class ApiInvoker:
    """
    调用者类
    负责接收一个task并执行它，它本身不应该存储task的信息，但需要存储task执行相关的信息
    完成调用日志记录
    Q：为什么会有这么两个类而不是在task中提供invoke方法
    A：task和它的调用是两回事，task不需要被记录，它的调用需要被记录--这不绝对，只是这个场景如此（调用的记录就是task的内容）
    """

    def __init__(self, task: Task):
        self.config = of_yaml(Environment.to_instance().to_config())
        self.task = task

    def to_token(self, timespan):
        token = self.config['appkey'] + timespan + self.config['seckey']
        md5 = hashlib.md5()
        md5.update(token.encode(encoding=encode))
        return md5.hexdigest().upper()

    def to_header(self):
        timespan = str(int(time.time()))
        return {'Token': self.to_token(timespan), 'Timespan': timespan}

    def invoke(self):

        url_req = self.task.to_request_url()
        params = self.task.params
        params['key'] = self.config['appkey']

        # logger.info(json.dumps(self.task, ensure_ascii=False, cls=TaskEncoder))

        r = requests.get(url=url_req,
                         headers=self.to_header(),
                         params=params)

        if r.status_code == 200:
            code = int(r.json()['Status'])
            self.task.code = code
            if code == 200:
                # self.task.data = json.dumps(str(r.content, encoding=encode))\
                #     .encode(encode)\
                #     .decode("unicode-escape")
                self.task.data = r.json()
                self.task.success = True
            else:
                self.task.message = error_code.get(str(code), '')
        else:
            self.task.code = r.status_code
            # self.task.message = error_code[r.status_code]

        # logger.info(json.dumps(self.task, ensure_ascii=False, cls=TaskEncoder))

        return self

    def to_task(self):
        return self.task
