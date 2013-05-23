#!/usr/bin/env python
#coding: utf8

import sys

from AC import trieKmp
from database import Database

reload(sys)
sys.setdefaultencoding('utf-8')

data = Database('data.db')
h = data.find_a()
N = len(h)
#print len(h)

while True:
    s = raw_input('input the keywords:')
    query = unicode(s)
    d = trieKmp.gao(query)
    fc = []
    for i in xrange(trieKmp.num):
        if d[i] == '0':
            continue
        fc.append(i)
    M = len(fc)
    print '分词结果为: ', 
    for ch in fc:
        print trieKmp.word[ch],
    print ''
    g = []
    for i in xrange(N):
        cnt = 0
        for j in fc:
            cnt += int(h[i][1][j])
        g.append([h[i], cnt])
    g.sort(cmp = lambda x, y: cmp(y[1], x[1]))
#    for i in xrange(10):
#        print g[i][1], 
    for i in xrange(5):
        #print g[i][0][0]
        arg = data.find_b(int(g[i][0][0]))
        print 'url:',  arg[0]
        print '标题:', arg[1]
        print '摘要:', arg[2]
        print '相关读:', g[i][1]
        print ''
