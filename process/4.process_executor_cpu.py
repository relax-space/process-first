'''
说明: 多进程运行时,同一个子进程可能会在多个cpu上运行
注: 本文件代码只能在linux环境下运行
    max_workers: 同一时刻,有多少线程在cpu上执行. 如果max_workers=4,cpu核数为16,只能说同一时刻最多只会4个线程在cpu上执行,实际上16个cpu可能都会工作,详细请看:https://www.cnblogs.com/edisonchou/p/5020681.html
    cpu_num: 返回此进程当前正在运行的 CPU的编号[编号从0开始]。这个方法只能在linux上使用,如何在windows上部署linux环境
'''
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import current_process

import psutil


def req1(count):
    process = psutil.Process(current_process().ident)
    res = set()
    for i in range(count):
        key = f'pid:{current_process().ident} cpu_id:{process.cpu_num()}'
        res.add(key)
    return res


def main1():
    count = 10000
    with ProcessPoolExecutor(max_workers=4) as exec:
        res = next(as_completed([exec.submit(req1, count)]))
        return res.result()


if __name__ == '__main__':
    print(main1())


'''
可以看到当count=100000并且max_workers=4时,有5个cpu运行了子进程的代码,大于了设置的4个
count为10000,输出:{'pid:506 cpu_id:10', 'pid:506 cpu_id:11'}
count为100000,输出:{'pid:510 cpu_id:2', 'pid:510 cpu_id:0', 'pid:510 cpu_id:1', 'pid:510 cpu_id:10'}
count为1000000,输出:{'pid:514 cpu_id:1', 'pid:514 cpu_id:2', 'pid:514 cpu_id:3', 'pid:514 cpu_id:10', 'pid:514 cpu_id:0'}
'''
