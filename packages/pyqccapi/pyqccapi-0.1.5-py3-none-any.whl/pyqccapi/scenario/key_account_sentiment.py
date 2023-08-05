from pyqccapi.constant import *
from pyqccapi.scenario.base_scenario import *
from pyqccapi.util.dates import *


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
    task = Task(method_id, params)
    return to_task_invoker(task) \
        .invoke() \
        .to_task()


def to_news_summary_list_at_date(id_uni: str, dt: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期的新闻概要列表
    :param id_uni:
    :param dt:
    :return:
    """
    method_id = '3a5dd06b-aec5-445d-9b91-82be4d5b884b'
    page_size = 50
    summary_list = []

    params = {
        'searchKey': id_uni,
        'startDate': dt,
        'endDate': dt,
        'pageSize': page_size,
        'pageIndex': 1
    }
    task = Task(method_id, params)
    t = to_task_invoker(task).invoke().to_task()

    if t.success:
        total = t.data['Paging']['TotalRecords']
    else:
        task.code = t.code
        task.message = t.message
        return summary_list

    page_count = total // page_size + 1

    for i in range(page_count + 1)[1:]:
        params['pageIndex'] = i
        task = Task(method_id, params)
        task = to_task_invoker(task).invoke().to_task()
        if task.success:
            for summary in task.data['Result']:
                summary['CategoryName'] = to_news_category_for_human(summary['Category'])
                summary_list.append(summary)

    return summary_list


def to_news_detail_by_summary(news: dict) -> dict:
    """
    根据新闻摘要，填充新闻具体内容，返回填充后的新闻对象
    :param news:
    :return:
    """
    t = to_news_detail_by_id(news['NewsId'])
    if t.success:
        news['Content'] = t.data['Result']['Content']
    return news


def to_news_detail_list_at_date(id_uni: str, dt: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期的新闻详情列表
    :param id_uni:
    :param dt:
    :return:
    """
    detail_list = []

    for summary in to_news_summary_list_at_date(id_uni, dt):
        detail_list.append(to_news_detail_by_summary(summary))

    return detail_list


def to_news_detail_list_by_period(id_uni: str, start: str, end: str) -> list:
    """
    根据统一社会信用代码，获取一个企业在给定日期范围内的新闻详情列表
    :param id_uni:
    :param start:
    :param end:
    :return:
    """
    period_list = []

    days_diff = to_days_diff(start, end)
    for i in range(days_diff):
        date_after = to_date_after(start, i)
        period_list += to_news_detail_list_at_date(id_uni, date_after)
    return period_list


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
