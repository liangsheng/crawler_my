#!/usr/bin/env python
#coding: utf8

import traceback
from threading import Thread, Lock
from Queue import Queue, Empty
import logging
from time import ctime, sleep

log = logging.getLogger('Main.threadPool')

class Worker(Thread):
    
    '''通用函数'''

    def __init__(self, threadPool):
        Thread.__init__(self)
        self.threadPool = threadPool
        self.daemon = True
        self.state = None
        self.start()

    def stop(self):
        self.state = 'STOP'

    def run(self):
        while 1:
            if self.state == 'STOP':
                break
            try:
                func, args, kargs = self.threadPool.getTask(timeout = 1)
            except Empty:
                continue
            try:
                self.threadPool.increaseRunsNum()
                #print 'PPPPP= ', self.threadPool.taskQueue.qsize(), self.threadPool.running
                #print self.name, func.__name__, 'begin time:', ctime()
                #print 'KKK', self.name
                func(*args, **kargs)
                #print self.name, func.__name__, 'end time:', ctime()
                self.threadPool.decreaseRunsNum()
                self.threadPool.taskDone()
            except Exception, e:
                #print traceback.format_exc()
               log.critical(traceback.format_exc())

class ThreadPool(object):

    '''最普通的多线程模型'''

    def __init__(self, threadNum):
        self.pool = []                 #线程池
        self.threadNum = threadNum     #线程数    
        self.running = 0               #正在run的线程数       
        self.taskQueue = Queue()       #任务队列
        self.lock = Lock()             #线程锁

    def startThreads(self):
        for _ in range(self.threadNum):
            self.pool.append(Worker(self))

    def stopThreads(self):
        for thread in self.pool:
            thread.stop()
            thread.join()
        del self.pool[:]

    def putTask(self, func, *args, **kargs):
        self.taskQueue.put((func, args, kargs))

    def getTask(self, *args, **kargs):
        task = self.taskQueue.get(*args, **kargs)
        return task

    def taskJoin(self, *args, **kargs):
        self.taskQueue.join()

    def taskDone(self, *args, **kargs):
        self.taskQueue.task_done()

    def increaseRunsNum(self):
        self.lock.acquire()             #锁住变量
        self.running += 1
        self.lock.release()

    def decreaseRunsNum(self):
        self.lock.acquire()             #锁住变量
        self.running -= 1
        self.lock.release()

    def getTaskLeft(self):
        return self.taskQueue.qsize() + self.running


#def add(x, y):
#    sleep(3)
#    return x + y;

#def mul(x, y):
#    sleep(2)
#    return x * y


#funcs = [add, mul]

#ss = ThreadPool(2)
#ss.startThreads()

#for i in funcs:
#    ss.putTask(i, *(1, 2))

#ss.stopThreads()
