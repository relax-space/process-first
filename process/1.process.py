'''
说明: 如果函数在执行时的进程id跟主进程id不一致,表明是多进程执行
'''
from multiprocessing import Process, Queue, current_process


def req1(param, return_queue: Queue):
    return_queue.put(f'子进程id:{current_process().ident}|参数:{param}')


def main1():
    return_queue = Queue()
    ps = [Process(target=req1, args=(1, return_queue)), Process(
        target=req1, args=(2, return_queue))]
    for i in ps:
        i.start()

    for i in ps:
        i.join()
    return [return_queue.get() for i in ps]


# 注: 多进程必须在__main__语句里执行
if __name__ == '__main__':
    print(f'主进程id:{current_process().ident}, {main1()}')

'''
输出: 可以看到,子进程跟主进程的id不一样
    主进程id:14456, ['子进程id:6804|参数:1', '子进程id:20220|参数:2']
'''
