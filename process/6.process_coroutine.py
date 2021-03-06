'''
说明：多进程 + 协程的例子
'''

import asyncio
from multiprocessing import Process, Queue, current_process

import aiofiles
from aiohttp import ClientSession


async def req1(session: ClientSession, i):
    async with session.get(f'http://httpbin.org/get?a={i}') as resp:
        async with aiofiles.open(f'data/{i}.log', mode='w', encoding='utf-8') as f:
            v = f'{str(current_process().name)} | {(await resp.json())["args"]["a"]}'
            await f.write(v)
            print(v)
            return i


async def main_async(req_list):
    async with ClientSession() as session:
        res = await asyncio.gather(*[req1(session, i) for i in req_list])
        return res


def main(req_list, res_value: Queue):
    res = asyncio.get_event_loop().run_until_complete(main_async(req_list))
    res_value.put(res)


def split(list, step):
    # 将大集合分割成小集合split([1,2,3,4,5,6], 2)结果是[[1,2],[3,4],[5,6]]
    length = len(list)
    return [list[i:i+step] for i in range(0, length, step)]


def main_process(req_list, process_count):
    raw_list = [i for i in range(req_list)]
    split_list = split(raw_list, process_count)
    res_value = Queue()
    ps = [Process(target=main, args=(i, res_value))
          for i in split_list]
    for i in ps:
        i.start()
    for i in ps:
        i.join()
    res_list = []
    for i in range(len(split_list)):
        res_list.extend(res_value.get())
    diff = set(raw_list) - set(res_list)
    assert not diff, f'异常的单号：{diff}'


if __name__ == '__main__':
    main_process(10, 3)

'''
输出：可以看出开了4个进程，Process-1处理了 [0,1,2],Process-2处理了 [3,4,5]....
    Process-1 | 2
    Process-1 | 0
    Process-2 | 3
    Process-1 | 1
    Process-3 | 6
    Process-3 | 8
    Process-2 | 5
    Process-4 | 9
    Process-2 | 4
    Process-3 | 7
'''
