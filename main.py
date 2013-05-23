#!/usr/bin/env python
#coding: utf8

import logging
import time
from datetime import datetime
from threading import Thread

from crawler import Crawler
from options import parser

class PrintProgress(Thread):

    ''' 每隔10秒在屏幕上打印爬虫进度信息'''

    def __init__(self, crawler):
        Thread.__init__(self)
        self.name = 'PrintProgress'
        self.beginTime = datetime.now()
        self.crawler = crawler
        #标记主线程是否等待该线程结束后再结束
        self.daemon = True

    def run(self):
        while 1:
            if self.crawler.isCrawling:
                print '---------------------------------------'
                print 'Crawling in depth %d' % self.crawler.currentDepth
                print 'already visited %d links' % self.crawler.getAlreadyVisitedNum()
                print '%d tasks reminding in thread pool.' % self.crawler.threadPool.getTaskLeft()
                print '---------------------------------------'
                time.sleep(10)

    def printSpeedingTime(self):
        self.endTime = datetime.now()
        print 'begins at: %s' % self.beginTime
        print 'ends at: %s' % self.endTime
        print 'speed time: %s\n' % (self.endTime - self.beginTime)
        print 'finished'


def configLogger(logFile, logLevel):
    ''' 配置logging的日志文件及日志等级记录'''
    logger = logging.getLogger('Main')
    LEVELS = {
        1: logging.CRITICAL,
        2: logging.ERROR,
        3: logging.WARNING,
        4: logging.INFO,
        5: logging.DEBUG,  #数字越大，记录越多
        }
    formatter = logging.Formatter(
        '%(asctime)s %(threadName)s %(levelname)s %(message)s')
    try:
        fileHandler = logging.FileHandler(logFile, 'w')
    except IOError, e:
        return False
    else:
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.setLevel(LEVELS.get(logLevel))
        return True;

def main():
    args = parser.parse_args()
    if not configLogger(args.logFile, args.logLevel):
        print '\nPermission denied :%s' % args.logFile
        print 'Please make sure you have the permission to save yhe log file\n'
    elif args.testSelf:
    	Crawler(args).selfTesting()
    else:
        log = logging.getLogger('Main')
        log.debug('Fuck')
        #print 'Hello World'
        #log = logging.getLogger('Main')
        #log.error('Fuck tourself')
        crawler = Crawler(args)
        printProgress = PrintProgress(crawler)
        printProgress.start()
        crawler.start()
        printProgress.printSpeedingTime()

if __name__ == '__main__':
    main()
