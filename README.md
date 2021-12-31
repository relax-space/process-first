# process-first

- 线程: 是cpu调度分配的最小单位
- 进程: 是操作系统资源分配（内存，显卡，磁盘）的最小单位一个进程可以有一个或多个线程
- 并行: 同一时刻cpu能处理2个以上的线程
- 超线程技术: 并行的线程数量通常是物理核数的两倍,比如8的cpu,可以同时执行16个线程
- python中的多进程: 虽然创建或者切换进程,比操作线程的价大,但是总算是可以用多核cpu,所以也可以考虑使用
- python中的协程: 单线程运行,可以并发的触发多个io任务,i运行的时候不需要cpu
- python中的多线程: 因为默认解释器cpython用到了GIL,导致同一时刻cpu只能执行一个线程,所以不能并行

``` python
gil不能并行的解释

books =['1','3','2']
books.sort()
print(books)

books.sort()代码中有gil锁, 所以同一时刻只能有一个线程执行这段代码.
cpu和线程的关系是1对多, 也就是说任意一个线程只能存在于1个cpu内核中
所以,同一时刻只能有1个cpu的内核在执行 带有gil锁的代码

```

## start

1. [多进程简单示例](docs/1.process.md)

2. [进程池简单示例](docs/2.process_executor.md)

3. [多进程:同一个进程在哪些cpu上运行过](docs/3.process_cpu.md)

4. [进程池:同一个进程在哪些cpu上运行过](docs/4.process_executor_cpu.md)

5. [进程共享变量加锁](docs/5.process_lock.md)

6. [多进程+协程的简单示例](docs/6.process_coroutine.md)

:ribbon: :ribbon: 读后有收获可以请作者喝咖啡：

<img src="https://images.gitee.com/uploads/images/2021/1226/125920_9f0e6151_9674723.png" width="60%"/>