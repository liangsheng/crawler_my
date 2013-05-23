#!/usr/bin/env python
#coding: utf8

from collections import deque

class ACmatch(object):

    """AC自动机的hash_map实现"""

    def __init__(self):
        #关键字列表
        self.word = [
            u'软件', u'学院', u'运动', u'运动会', u'西安', u'交通', u'大学', u'郑南宁', u'校长', u'仲英', u'书院'
        ]
        self.num = len(self.word)
        #最大节点数
        self.N = len(self.word) * 4
        #用hash_map存储的儿子节点
        self.chd = [dict() for _ in xrange(self.N)]
        #末尾节点
        self.end = 1
        #失败节点
        self.fail = [0] * self.N
        #标记节点的关键信息
        self.wv = [set() for _ in xrange(self.N)]
        self.start()

    def start(self):
        size = len(self.word)
        for i in xrange(size):
            self.add(self.word[i], i)
        self.build()

    def add(self, s, val):
        p = 0
        for i in s:
            if not i in self.chd[p]:
                self.chd[self.end].clear()
                self.chd[p][i] = self.end
                self.end += 1
            p = self.chd[p][i]
        self.wv[p].add(val);

    def build(self):
        q = deque()
        self.fail[0] = 0
        for u in self.chd[0]:
            v = self.chd[0][u]
            self.fail[v] = 0;
            q.append(v)
        while len(q) != 0:
            p = q.popleft()
            for u in self.chd[p]:
                v = self.chd[p][u]
                self.fail[v] = 0
                t = p
                while t != 0:
                    t = self.fail[t]
                    if u in self.chd[t]:
                        self.fail[v] = self.chd[t][u]
                        for i in xrange(self.num):
                            self.wv[v] |= self.wv[self.fail[v]]
                        break
                q.append(v)


    def gao(self, text):
        #print 'text=', text
        p = 0
        ans = dict()
        for ch in text:
            if ch in self.chd[p]:
                u = self.chd[p][ch]
                for w in self.wv[u]:
                    if w in ans:
                        ans[w] += 1
                    else:
                        ans[w] = 1
                p = u
            else:
                t = p
                while t != 0:
                    t = self.fail[t]
                    if ch in self.chd[t]:
                        u = self.chd[t][ch]
                        for w in self.wv[u]:
                            if w in ans:
                                ans[w] += 1
                            else:
                                ans[w] = 1
                        p = u
                        break
                if t == 0:
                    if ch in self.chd[0]:
                        u = self.chd[0][ch]
                        for w in self.wv[u]:
                            if w in ans:
                                ans[w] += 1
                            else:
                                ans[w] = 1
                        p = u
                    else:
                        p = 0
        res = []
        for i in xrange(self.num):
            if i in ans:
                if ans[i] > 9:
                    u = 9
                else:
                    u = ans[i]
                res.append(str(u))
            else:
                res.append(str(0))
        return ''.join(res)



#a = ACmatch()
#text = u"""
#4月24日上午，西安交大管理学院举行“秦势――经济强与美丽陕西”暨西部经济学派论坛、《中国关中-天水发展报告（2012）》和《2013中国社会管理发展报告》新闻发布会。发布会由西安交通大学、中国民主建国会陕西委员会经济委员会、陕西师范大学中国西部商学研究中心、华商报共同主办，由陕西省社会科学院、西北大学中国西部经济发展研究中心、陕西省《资本论》研究会、陕西省经济学会、陕西省外国经济学说研究会、陕西省金融学会作为学术支持单位。陕西省政协副主席、中国民主建国会陕西省委员会主委李冬玉，陕西省金融办副主任李忠民教授，西安交大汪应洛院士及李佩成院士、著名经济学家何炼成教授与来自政府研究部门、省市民建和高等院校的160余领导、专家学者、学生参加发布会。《2013中国社会管理发展报告》新闻发布会    大会由陕西省金融办副主任、西安交大管理学院兼职教授李忠民教授主持。陕西省政协副主席李冬玉作大会主题发言。西安交大科研院副院长兼人文社科处处长贾毅华、管理学院党委书记孙卫教授分别代表学校和学院致辞。贾毅华副院长在致辞中强调《中国社会管理发展报告》是由西安交通大学组织，以教育部软科学研究基地“中国管理问题研究中心”为载体，从2011年起开始编辑出版的年度报告，由科学出版社出版。《中国社会管理发展报告》致力于围绕中国经济社会发展中的重大问题，有计划地组织学校及其他相关优势研究力量，面向政府部门提交政策建议，树立西安交通大学人文社会科学研究品牌，提高我校教师在社会各界的知名度，是学校实施“人文社科名家推进计划”的重要内容之一。西安交大管理学院冯耕中教授介绍了《2013中国社会管理发展报告》的撰写背景及具体内容。该报告以西安交通大学人文社会科学已有的研究力量为依托，立足中国国情和社会实践，从公共管理、经济安全和信息管理三个视角出发，由61个作者共同努力，编写了18份专题报告，涉及我国人口与社会发展、医疗卫生、社会保障、国家审计管理、科研管理、教育、世界经济与我国产业安全、金融安全、食品安全、上市公司风险控制、煤炭产业升级、新生代员工管理、大数据管理、社会化媒体与社会管理、政务微博与管理创新、大宗商品电子交易市场管理等系列主题。会上，发布了《中国关中―天水经济区发展报告（2012）》。该报告是教育部哲学社会科学发展报告首批资助项目，由陕西师范大学中国西部商学研究中心大关中发展研究所组织全国长期研究关中天水经济区及周边区域
#"""
#d = a.gao(text)
#print d

trieKmp = ACmatch()
