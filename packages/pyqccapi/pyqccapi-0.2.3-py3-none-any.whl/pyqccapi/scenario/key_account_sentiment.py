from multiprocessing.pool import Pool

from pyqccapi.constant import *
from pyqccapi.scenario.base_scenario import *

# from pyqccapi.util.dates import *

"""
获取重点企业的舆情信息，用于进一步文本挖掘
"""


def to_news_detail_by_id(id_news: str) -> Task:
    """
    根据新闻id，获取新闻详情
    :param id_news:
    :return:
    """
    method_id = '7501bee3-4242-4e72-aec3-4ed756c8e6a0'
    params = {
        'id': id_news
    }
    return to_task_invoker(Task(method_id, params)).invoke().to_task()


def to_news_summary_list_by_period(uni_id: str,
                                   start: str,
                                   end: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期范围的新闻概要列表
    :param end:
    :param start:
    :param uni_id:
    :return:
    """

    method_id = '3a5dd06b-aec5-445d-9b91-82be4d5b884b'
    page_size = 50
    summary_list = []
    params = {
        'searchKey': uni_id,
        'startDate': start,
        'endDate': end,
        'pageSize': page_size,
        'pageIndex': 1
    }

    task = to_task_invoker(Task(method_id, params)).invoke().to_task()

    if task.success:
        for summary in task.data['Result']:
            summary['uni_id'] = uni_id
            summary['CategoryName'] = to_news_category_for_human(summary['Category'])
            summary_list.append(summary)
        if task.data['Paging'] is not None:
            total = task.data['Paging']['TotalRecords']
        else:
            return summary_list
    else:
        return summary_list

    page_count = total // page_size + 1
    if page_count > 1:
        for i in range(page_count + 1)[2:]:
            params['pageIndex'] = i
            task = to_task_invoker(Task(method_id, params)).invoke().to_task()
            if task.success:
                for summary in task.data['Result']:
                    summary['uni_id'] = uni_id
                    summary['CategoryName'] = to_news_category_for_human(summary['Category'])
                    summary_list.append(summary)

    return summary_list


def to_news_detail_by_summary(news: dict) -> dict:
    """
    根据新闻摘要，填充新闻具体内容，返回填充后的新闻对象
    :param news:
    :return:
    """
    task = to_news_detail_by_id(news['NewsId'])
    if task.success:
        news['Content'] = task.data['Result']['Content']
    return news


def to_news_detail_list_by_period(uni_id_list: list,
                                  start: str,
                                  end: str) -> list:
    """
    根据统一社会信用代码列表，获取企业在给定日期范围的新闻详情列表，使用串行
    :param end:
    :param start:
    :param uni_id_list:
    :return:
    """
    detail_list = []

    for uni_id in uni_id_list:
        for summary in to_news_summary_list_by_period(uni_id, start, end):
            detail_list.append(to_news_detail_by_summary(summary))

    return detail_list


def to_news_detail_list_by_period_parallel(uni_id_list: list,
                                           start: str,
                                           end: str) -> list:
    """
    根据统一社会信用代码列表，获取企业在给定日期范围的新闻详情列表，使用并行
    :param uni_id_list:
    :param end:
    :param start:
    :return:
    """
    futures = []
    detail_list = []

    pool = Pool(os.cpu_count())

    for i, uni_id in enumerate(uni_id_list):
        futures.append(pool.apply_async(func=to_news_detail_list_by_period, args=([uni_id], start, end)))

    pool.close()
    pool.join()

    for future in futures:
        detail_list += future.get()

    return detail_list


# def to_news_detail_list_by_period(id_uni: str, start: str, end: str) -> list:
#     """
#     根据统一社会信用代码，获取一个企业在给定日期范围内的新闻详情列表
#     :param id_uni:
#     :param start:
#     :param end:
#     :return:
#     """
#     period_list = []
#
#     days_diff = to_days_diff(start, end)
#     for i in range(days_diff):
#         date_after = to_date_after(start, i)
#         period_list += to_news_detail_list_at_date(id_uni, date_after)
#     return period_list


def to_news_category_for_human(news_categories: str) -> str:
    """
    将新闻类别翻译为人类能看懂的中文
    :param news_categories:
    :return:
    """
    name_list = []
    if news_categories.find(',') >= 0:
        for category in news_categories.split(','):
            name_list.append(news_category.get(category))
    else:
        if len(news_categories) > 0:
            name_list.append(news_category.get(news_categories))
    return ','.join(name_list)
