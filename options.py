#!/usr/bin/env python
#coding: utf8

"""
> options.py
> 该模块定义了程序接受的命令行参数
"""

import argparse

_default = dict (
    logFile = 'spider.log',
    dbFile = 'data.db',
	logLevel = 5,
    depth = 2,
    threadNum = 10,
    )

def positiveInt(rawValue):
    errorInfo = 'Must be a positive integer.'
    try:
        value = int(rawValue)
    except ValueError:
        raise argparse.ArgumentTypeError(errorInfo)
    if value < 1:
        raise argparse.ArgumentTypeError(errorInfo)
    else:
        return value

def url(rawValue):
    if not rawValue.startswith('http'):
        value = 'http://' + rawValue
    else: value = rawValue
    return value


parser = argparse.ArgumentParser(description = 'A web crawler for xjtu')

parser.add_argument('-u', type = url, required = True, metavar = 'URL', dest = 'url', help = 'the starting url')

parser.add_argument('--d', type = positiveInt,  choices = [1, 2, 3, 4, 5], metavar = 'DEPTH', default = _default['depth'], dest = 'depth', help = 'the depth for crawlering')

parser.add_argument('--thread', type = positiveInt, metavar = 'THREAD', default =_default['threadNum'], dest = 'threadNum', help = 'the depth for crawlering')

parser.add_argument('--logFile', type = str, metavar = 'FILE', default = _default['logFile'], dest = 'logFile', help = 'the name of logfile, default is %s' % _default['logFile'])

parser.add_argument('--dbFile', type = str, metavar = 'FILE', default = _default['dbFile'], dest = 'dbFile', help = 'the name of dbfile, default is %s' % _default['dbFile'])

parser.add_argument('--logLevel', type = int, choices = [1, 2, 3, 4, 5], default = _default['logLevel'], dest = 'logLevel', help = 'the level if logging details. larger number record more details. default is %d' % _default['logLevel'])

parser.add_argument('--testSelf', action = 'store_true', dest = 'testSelf', help = 'Crawler self test')

def main():
    args = parser.parse_args()
    print args

if __name__ == '__main__':
    main()
