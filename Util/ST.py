#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 hanwei <hanwei20082123@163.com>


'''
自己编写的一些文本特征统计的函数
'''


import sys
import jieba
import jieba.posseg as pseg
from math import log

jieba.enable_parallel(6)
vec_add = lambda a, b: tuple([x + y for x, y in zip(a, b)])  # 定义向量的加法
top_path = u"清水河畔"


'''
统计信息熵：输入二元词统计dict和一元词集合，返回左右信息熵
'''


def Entropy(bfreq, term):
    LED0 = dict()  # 先统计的其实是二元序列中成对出现的次数
    RED0 = dict()
    for p, f in bfreq.items():
         # 左
        temp_value = LED0.get(p[1])
        LED0[p[1]] = temp_value and temp_value + 1 or 1
        # 右
        temp_value = RED0.get(p[0])
        RED0[p[0]] = temp_value and temp_value + 1 or 1

    LED00 = dict()
    RED00 = dict()
    for w in term:
        temp_LED0 = 0.0
        for p, fp in bfreq.items():
            if p[1] == w:
                nl = float(LED0[w])
                temp_LED0 = temp_LED0 - (float(fp) / nl) * log(float(fp) / nl, 2)
            LED00[w] = temp_LED0
        temp_RED0 = 0.0
        for p, fp in bfreq.items():
            if p[0] == w:
                nr = RED0[w]
                temp_RED0 = temp_RED0 - (float(fp) / nr) * log(float(fp) / nr, 2)
            RED00[w] = temp_RED0
    return LED00, RED00

'''
统计词频：输入list型的词序列，返回dict型的词频
'''


def TF(terms):
    ufreq = dict()
    for word in terms:
        temp_value = ufreq.get(word)
        ufreq[word] = temp_value and temp_value + 1 or 1
    return ufreq

'''
统计二元词频：输入list型的词序列，返回dict型的二元词频
'''


def DTF(terms):
    bfreq = dict()
    first_flag = 1
    for word in terms:
        if first_flag:
            first_flag = 0
            temp_pre = word
        else:
            temp_now = word
            temp_pair = (temp_pre, temp_now)
            temp_value = bfreq.get(temp_pair)
            bfreq[temp_pair] = temp_value and temp_value + 1 or 1
            temp_pre = temp_now
    return bfreq


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')  # python2.7是基于ascii去处理字符流，当字符流不属于ascii范围内，就会抛出异常（ordinal not in range(128)）。
    readin = u'美女坐我对面我在食堂对面吃饭'

# 1、美女坐我对面我在食堂吃饭，一边用餐，一边玩手机。这时，一个找不到空桌的美女坐在了我的对面，顿时，我紧张起来。但为了不失态，我强装镇定。本想文雅的吃一口饭，可一激动，把手机放嘴里了……2、赤裸裸的暗示
# 某天晚上去KTV参加一心仪男生的生日party，买了一条围巾做礼物。出门前老妈怕我冻着硬是要我穿秋裤，其实年轻人并不怕冷，于是到了KTV立马溜进厕所把秋裤脱了放进塑料袋装包里。回家后，发现围巾还包里，总觉得哪里不对劲，Oh
# shit！难道我送给他的是秋裤！尼玛还是大红色的啊！囧。。

    words = pseg.cut(readin)
    terms = list()
    term = set()
    for w in words:
        terms.append(w.word)
        term.add(w.word)
        '''
        词频统计测试
        '''
    ufreq = TF(terms)
    # for w, f in ufreq.items():
    #     print w, f, '\n'

    '''
    二元词频统计测试
    '''
    bfreq = DTF(terms)
    # for p, f in bfreq.items():
    #     print p[0], p[1], f, '\n'

    '''
    信息熵测试
    '''
    LE, RE = Entropy(bfreq, term)
    for w, le in LE.items():
        print w, le, '\n'
    for w, re in RE.items():
        print w, re, '\n'
