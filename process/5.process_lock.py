'''
说明: 对共享变量做写操作的时候,需要加锁, 因为两个线程同时操作一个内存变量会导致数据不准确
推荐: 推荐使用main2 或 main4的方法上锁
'''

import time
from multiprocessing import Lock, Process, RawValue, Value


def req1(res_int, count):
    for i in range(count):
        time.sleep(0.05)
        res_int.value += 1


def main1(count):
    res_int = Value('i', 0)
    procs = [Process(target=req1, args=(res_int, count)) for i in range(10)]
    for i in procs:
        i.start()

    for i in procs:
        i.join()
    return res_int.value


def req2(res_int, count, lock):
    for i in range(count):
        time.sleep(0.05)
        with lock:
            res_int.value += 1


def main2(count):
    res_int = Value('i', 0)
    lock = Lock()
    procs = [Process(target=req2, args=(res_int, count, lock))
             for i in range(10)]
    for i in procs:
        i.start()

    for i in procs:
        i.join()
    return res_int.value


def req3(res_int, count):
    for i in range(count):
        time.sleep(0.05)
        # 对于 Value对象 来说,他可以获取锁
        with res_int.get_lock():
            res_int.value += 1


def main3(count):
    res_int = Value('i', 0)
    procs = [Process(target=req3, args=(res_int, count))
             for i in range(10)]
    for i in procs:
        i.start()

    for i in procs:
        i.join()
    return res_int.value


class Counter:
    def __init__(self, init_value):
        self.val = RawValue('i', init_value)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    @property
    def value(self):
        return self.val.value

    @value.setter
    def value(self, v):
        with self.lock:
            self.val.value = v


def req4(res_int, count):
    for i in range(count):
        time.sleep(0.05)
        res_int.increment()


def main4(count):
    res_int = Counter(0)
    procs = [Process(target=req4, args=(res_int, count))
             for i in range(10)]
    for i in procs:
        i.start()

    for i in procs:
        i.join()
    return res_int.value


if __name__ == '__main__':
    count = 50
    print(f'不上锁: main1的结果{main1(count)}')
    print(f'上锁(推荐): main2的结果{main2(count)}')
    # 据说这个没有第2或4快
    print(f'上锁(不推荐): main3的结果{main3(count)}')
    print(f'上锁(推荐): main4的结果{main4(count)}')

'''
不上锁: main1的结果248
上锁(推荐): main2的结果500
上锁(不推荐): main3的结果500
上锁(推荐): main4的结果500
'''
