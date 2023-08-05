import os
from multiprocessing.pool import Pool

from pyqccapi.scenario.base_scenario import *
from pyqccapi.util import progress_bar

"""
企业客户信息治理
根据企业名称等线索获取统一社会信用代码
"""


def to_uni_id_by_name(name: str) -> str:
    """
    根据企业名称，查询企业统一社会代码
    :param name:
    :return:
    """
    method_id = '8a577c55-6fa9-430a-ab71-d54630713244'
    params = {
        'searchKey': name
    }
    task = to_task_invoker(Task(method_id, params)).invoke().to_task()
    if task.success:
        return task.data['Result'][0]['CreditCode']
    return ''


def to_corp_info(corp: dict) -> dict:
    """
    根据企业名称，填充企业统一社会信用代码，返回企业对象
    :param corp:
    :return:
    """
    corp['id_uni'] = to_uni_id_by_name(corp['name'])
    return corp


def to_corp_list(corp_list: list) -> list:
    """
    根据企业列表，填充统一社会信用代码，使用串行
    :param corp_list:
    :return:
    """
    new_corp_list = []
    for corp in corp_list:
        new_corp_list.append(to_corp_info(corp))
    return new_corp_list


def to_corp_list_parallel(corp_list: list) -> list:
    """
    根据企业列表，填充统一社会信用代码，使用并行
    :param corp_list:
    :return:
    """

    futures = []
    new_corp_list = []

    pool = Pool(os.cpu_count())

    total = len(corp_list) - 1
    for i, corp in enumerate(corp_list):
        progress_bar.show(i / total)
        futures.append(pool.apply_async(func=to_corp_info, args=(corp,)))

    pool.close()
    pool.join()

    total = len(futures) - 1
    for i, future in enumerate(futures):
        progress_bar.show(i / total)
        new_corp_list.append(future.get())

    return new_corp_list


def purify_corp_name(name: str) -> str:
    """
    清理客户注册时的附加信息，如 ****企业(专户)
    :param name:
    :return:
    """
    name = name.strip()
    if name.endswith(")") or name.endswith("）"):
        pos = name.rfind("(")
        if pos < 0:
            pos = name.rfind("（")
        if pos >= 0:
            return name[0:pos]
    return name
