from multiprocessing import Process, Queue, cpu_count

from pyqccapi.task.task_invoker import *

TASK_QUEUE = Queue(ctx=AsyncTask)
RESULT_QUEUE = Queue(ctx=AsyncTask)


def batch_task_producer_proxy(task_list: list[AsyncTask]):
    for task in task_list:
        task_producer_proxy(task)


def task_producer_proxy(task: AsyncTask):
    TASK_QUEUE.put(task)


def task_consumer():
    while True:
        task = TASK_QUEUE.get()
        if isinstance(task, AsyncTask):
            task = ApiInvoker(task).invoke().to_task()
            RESULT_QUEUE.put(task)


if __name__ == '__main__':

    process_list = []

    for i in range(cpu_count()):
        process_list.append(Process(target=task_consumer, args=()))

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
