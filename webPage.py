#!/usr/bin/env python
#coding: utf8

"""
> webPage.py
> 该模块用于下载网页源代码，允许自定义header和使用代理
"""

import re
import logging

import requests

log = logging.getLogger('Main.WebPage')

class WebPage(object):

    def __init__(self, url):
        self.url = url
        self.pageSource = None
        self.customHeaders()

    def customHeaders(self, **kargs):   #自定义头部**kargs
        self.headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset' : 'gb2312,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            #模拟浏览器访问
            'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
            #防止反倒链
            'Referer' : self.url,
        }
        self.headers.update(kargs)

    def judge(self, r):    #只处理html源码
        #print 'okkkkkk?'
        if r.status_code == requests.codes.ok:
            if 'html' in r.headers['Content-Type']:
                return True
        return False

    def gaoEncoding(self, r):
        #request会自动处理编码，若无则指定为'ISO-8859-1'
        #需要解析源码中的meta标签
        if r.encoding == 'ISO-8859-1':
            charset_re = re.compile("((^|;)\s*charset=)([^\"]*)", re.M)
            charset = charset_re.search(r.text)
            charset = charset and charset.group(3) or None
            r.encoding = charset

    def fetch(self, retry = 1, proxies = None):
        try:
            #print 'FFFFF', self.url
            r = requests.get(self.url, headers = self.headers, timeout = 5)
            #print r.headers['Content-Type'], 'ooooooooook'
            #print 'liangsheng', judge(r)
            #print r.text, 'trrrrr=', retry
            if self.judge(r):
                #print 'OPOPOPOPOPO'
                self.gaoEncoding(r)
                self.pageSource = r.text
                return True
            else:
                #print 'LLLLLLL', self.url
                log.warning('Page not avaliable, Status code: %d URL: %s\n' % (r.status_code, self.url))
        except Exception, e:
            #print 'eeeee=', e
            if retry > 0:  #超时，用代理
                my_proxies = {
                        "http": "http://127.0.0.1:8087",
                        "https": "http://127.0.0.1:8087",
                }
                return self.fetch(retry - 1, proxies = my_proxies)
            else:
                #print 'KKKKKK'
                log.debug(str(e) + 'URL %s\n' % self.url)
        return None

    def getDatas(self):
        return self.url, self.pageSource
