#!/usr/bin/env python
#coding: utf8

"""
> crawler.py
> 爬虫的具体实现
"""

import logging
from collections import deque
import re
import traceback
import time
from urlparse import urljoin, urlparse
from locale import getdefaultlocale

from bs4 import BeautifulSoup

from webPage import WebPage
from database import Database
from threadPool import ThreadPool
from AC import trieKmp

log = logging.getLogger('Main.crawler')


class Crawler(object):

    def __init__(self, args):
        #指定网页深度
        self.depth = args.depth
        #表示爬虫深度，从1开始
        self.currentDepth = 1
        #数据库
        self.database = Database(args.dbFile)
        #线程池，指定线程数
        self.threadPool = ThreadPool(args.threadNum)
        #已经访问的链接
        self.visitedHrefs = set()
        #待访问的页面
        self.unvisitedHrefs = deque()
        #首个待访问的页面
        self.url = args.url
        self.unvisitedHrefs.append(args.url)
        #标记爬虫是否开始执行
        self.isCrawling = False

    def isDatabaseAvaliable(self):
        if self.database.isConn():
            return True
        return False

    def _saveTaskResults(self, my_web):
        #只过滤包含正文的网页
        str = '.*\w{16}\.((html)|(shtml))'
        url, pageSource = my_web.getDatas()
        r = re.search(str, url)
        if r is not None:        
           soup = BeautifulSoup(pageSource)
           if soup.h2 is not None:
               title = unicode(soup.h2.string)
           elif soup.p is not None:
               title = unicode(soup.p.string)
           else:
               title = 'no title'
           text = ''
           for i in soup.find_all('p'):
              text += unicode(i.get_text())           
           #tmp = trieKmp.gao(title + text)
           t1 = trieKmp.gao(title)
           t2 = trieKmp.gao(text)
           tmp = []
           for i in xrange(len(t1)):
               if t1[i] != '0':
                   tmp.append('9')
               else:
                   tmp.append(t2[i])
           res = ''.join(tmp)
           #print 'res=', res          
          # print 'text=', text, 'tmp=', tmp
          # print 'tmp=', tmp
           self.database.saveData(url, title, text[: 40], res)
        return 0

    def _getAllHrefsFromPage(self, url, pageSource):
        '''用beautifulsoup解析源码，得到有效连接'''
        hrefs = []
        soup = BeautifulSoup(pageSource)
        results = soup.find_all('a', href = True)
        for a in results:
            #防止中文连接，encode转为utf8
            href = a.get('href').encode('utf8')
            if not href.strip().startswith('http'):           #去除前后多余的空格
                href = urljoin(url, href)
            hrefs.append(href)
        return hrefs

    def _isHttpOrHttpsProtocol(self, href):
        '''只处理http，https连i接'''
        protocal = urlparse(href).scheme
        if protocal == 'http' or protocal == 'https':
            if not(self.url in href):
                return False
            if '.jpg' in href:
                return False
            return True
        return False

    def _isHrefRepeated(self, href):
        '''去掉重复的网页'''
        if href in self.visitedHrefs or href in self.unvisitedHrefs:
            return True
        return False

    def _addUnvisitedHrefs(self, my_web):
        '''添加未访问连接'''
        url, pageSource = my_web.getDatas()
        hrefs = self._getAllHrefsFromPage(url, pageSource)
        for href in hrefs:
            if self._isHttpOrHttpsProtocol(href):
                if not self._isHrefRepeated(href):
                    self.unvisitedHrefs.append(href)

    def getAlreadyVisitedNum(self):
        '''获得已经访问的网页的数目'''
        return len(self.visitedHrefs) - self.threadPool.getTaskLeft()

    def _taskHandler(self, url):
        '''以_开头的函数是放在队列里供线程提取用的'''
        my_web = WebPage(url)
        #print 'Fuck', my_web.fetch()
        if my_web.fetch():
            #print 'has visited %s' % url
            self._saveTaskResults(my_web)
            self._addUnvisitedHrefs(my_web)

    def _assignCurrentDepthTasks(self):
        '''分配任务，该操作不阻塞'''
        while self.unvisitedHrefs:
            url = self.unvisitedHrefs.popleft()
            #分配给任务队列
            self.threadPool.putTask(self._taskHandler, url)
            self.visitedHrefs.add(url)

    def stop(self):
        self.isCrawling = False
        self.threadPool.stopThreads()
        self.database.close()

    def start(self):
        print '\nstart crawling', self.url
        self.isCrawling = True
        self.threadPool.startThreads()
        while self.currentDepth < self.depth + 1:
            #分配任务（该操作不阻塞）
            self._assignCurrentDepthTasks()
            #等待该层任务结束
            #print 'sssssss'        
            #self.threadPool.taskJoin()
            while self.threadPool.getTaskLeft():
                #print self.threadPool.taskQueue.qsize()
                time.sleep(8)
            #print 'eeeeee'
            print 'depth %d finished. totally visited %d links.\n' % (self.currentDepth, len(self.visitedHrefs))
            log.info('depth %d finished. totally visited %d links.\n' % (self.currentDepth, len(self.visitedHrefs)))
            self.currentDepth += 1
        self.stop()

    def selfTesting(self):
        url = 'http://www.baidu.com'
        print '\nVisiting www.baidu.com using directly'
        my_web = WebPage(url)
        pageSource = my_web.fetch()
        #测试网络链接
        if pageSource == None:
            print 'please check your network'
        elif not self.isDatabaseAvaliable():
            print 'please make sure you have the permission to save data: %s\n' % args.dbFile
        else:
            self._saveTaskResults(my_web)
            print 'save data successfully'
            print 'seems all is ok'
