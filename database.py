#!usr/bin/env python
#coding: utf8

"""
> database.py
> 该模块主要提供爬虫所需要的sqlite数据库的创建，连接，断开等功能
"""

import sqlite3

class Database(object):
    
    def __init__(self, dbFile):
        try:
            #设置事务隔离级别, 每次修改自动提交, 多线程共用
            self.conn = sqlite3.connect(dbFile, isolation_level = None, check_same_thread = False)
            self.conn.execute('''CREATE TABLE IF NOT EXISTS
                            Webpage (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            url TEXT,
                            title TEXT, 
                            pageSource TEXT,
                            keyword TEXT)''') 
        except Exception, e:
            self.conn = None

    def isConn(self):
        if self.conn:
            return True
        else:
            return False

    def saveData(self, url, title, pageSource, keyword):
        if self.conn:
            sql = '''INSERT INTO Webpage (url, title, pageSource, keyword) VALUES (?, ?, ?, ?);'''
            self.conn.execute(sql, (url, title, pageSource, keyword) )
        else :
            raise sqlite3.OperationalError, 'Database is not connected. Can not save Data!'

    def close(self):
        if self.conn:
            self.conn.close
        else:
            raise sqlite3.OperationalError, 'Database is not connected.'

    def find_a(self):
        c = self.conn.cursor()
        c.execute('''select id, keyword from Webpage''')
        return c.fetchall()

    def find_b(self, x):
        c = self.conn.cursor()
        c.execute('select url, title, pageSource from Webpage where id = %d' % x)
        return c.fetchone()    

#s = Database('data.db')
#for i in s.find_b(1):
#    print unicode(i)
