'''
说明:通过进程池实现多进程开发
'''
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import current_process


def req1(param):
    return f'{current_process().ident} |{param}'


def main1(param):
    with ProcessPoolExecutor(max_workers=2) as exec:
        return list(exec.map(req1, param))


def main2(param):
    with ProcessPoolExecutor(max_workers=2) as exec:
        futures = []
        for i in param:
            futures.append(exec.submit(req1, i))
        return [i.result() for i in as_completed(futures)]


if __name__ == '__main__':
    param = [1, 2]
    print(f'map方式: 主进程id:{current_process().ident},子进程id:{main1(param)}')
    print(f'submit方法: 主进程id:{current_process().ident},子进程id:{main2(param)}')

'''
输出: 可以看到,子进程跟主进程的id不一样,另外:因为计算量小,调用两次req1,只用到了一个进程16064
    map方式: 主进程id:21488,子进程id:['16388 |1', '16388 |2']
    submit方法: 主进程id:21488,子进程id:['11144 |1', '11144 |2']
'''
