#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 hanwei <hanwei20082123@163.com>

# 本文参考下面的论文实现的
# 陈飞,刘奕群,魏超,张云亮,张敏,马少平.基于条件随机场方法的开放领域新词发现.软件学报,2013,24(5):
# 1051−1060. http://www.jos.org.cn/1000-9825/4254.htm

# 可以将各文档直接拼接起来，文档之间加一个空字符''

import os
from os.path import join
import sys
from math import log

import chardet
import jieba
import jieba.posseg as pseg

from Util.ST import Entropy
from Util.ST import TF
from Util.ST import DTF
# import Util.CH as UCH    #中文字符数统计

jieba.enable_parallel(6)
vec_add = lambda a, b: tuple([x + y for x, y in zip(a, b)])  # 定义向量的加法
top_path = u"清水河畔"

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')  # python2.7是基于ascii去处理字符流，当字符流不属于ascii范围内，就会抛出异常（ordinal not in range(128)）。
    result = list()

    '''
    一些用于存储统计量的容器
    '''

    # z = collections.OrderedDict()    排序字典

    ufreqc = dict()  # [[term:[doc,freq]]    全局一元统计
    bfreqc = dict()  # [[(term0,term1):[doc,freq]]    全局二元统计
    TFc = dict()  # 全局词频
    DTFc = dict()  # 全局二元词频
    DF = dict()  # 一元词文档频率
    DDF = dict()  # 二元词文档频率
    LEDc = dict()  # 全语料库左信息熵
    REDc = dict()  # 全语料库右信息熵
    LEDd = dict()  # 各文档平均后的左信息熵
    REDd = dict()  # 各文档平均后的右信息熵
    IDF = dict()  # 按论文中的公式计算得到的IDF
    # IFA 在标记过程中计算就是
    LEDM = dict()  # 平均左信息熵
    REDM = dict()  # 平均右信息熵
    # MI互信息

    termc = set()  # 记录本语料库出现的词语集合
    wordc = list()  # 记录本语料库词序列
    result = list()  # 最终的标注结果，用N×14的矩阵表示
    D = 0  # 文档数
    try:
        f1 = open('./temp1', 'w')
        for novel in os.listdir(top_path):
            with open(join(top_path, novel)) as f:
                str_for_dect = f.read(1024)
                encoding = chardet.detect(str_for_dect)['encoding']
                f.seek(0)
                readin = f.read().decode(encoding, 'ignore')
                words = pseg.cut(readin)

            termd = set()  # 记录本文档的词语集合
            wordd = list()  # 记录本文档的单词序列
            for w in words:
                # f1.write(w.word)
                # f1.write(u'\t')
                # f1.write(w.flag)
                # f1.write(u'\t')
                # f1.write(str(len(w.word)))
                # f1.write(u'\n')

                # 迭代量统计
                wordd.append(w.word)
                wordc.append(w.word)
                termd.add(w.word)
                termc.add(w.word)

            '''
            本文档统计
            '''
            TFd = TF(wordd)
            DTFd = DTF(wordd)
            LEDd, REDd = Entropy(DTFd, termd)
            '''
            本文档标记
            '''
            for w in words:
                # 还可以查询搜狗的新词表，就在这里进行存储。也可以单独弄
                result.append(
                    [w.word, len(w.word), w.flag, 0, 0, 0, 0, 0, TFd.get(w.word), LEDd.get(w.word), REDd.get(w.word), 0, 0])

            '''
            全局统计
            '''
            # 统计一元词文档频率和变形的TF
            for w, f in TFd.items():
                temp_value = DF.get(w)
                DF[w] = temp_value and temp_value + 1 or 1

                # temp_value_pair = ufreqc.get(w)  # 还可以构造对象替换数组方式
                # if temp_value_pair:
                #     temp_value_pair = vec_add(temp_value_pair, [1, f])
                # else:
                #     temp_pair = [1, f]
                #     ufreqc[w] = temp_pair
            # 统计二元词文档频率、DTF和变形的DTF
            for p, f in DTFd.items():
                temp_value = DDF.get(p)
                DDF[p] = temp_value and temp_value + 1 or 1

                temp_value = DTFc.get(p)
                DTFc[p] = temp_value and temp_value + 1 or 1

                # temp_value_pair = bfreqc.get(p)
                # if temp_value_pair:
                #     temp_value_pair = vec_add(temp_value_pair, [1, f])
                # else:
                #     temp_pair = [1, f]
                #     bfreqc[p] = temp_pair

                '''
                平均左右信息熵计算
                '''
                for t in termd:
                    temp_value = LEDM.get(t)
                    LEDM[t] = temp_value and temp_value + LEDd[t] or LEDd[t]
                    temp_value = REDM.get(t)
                    REDM[t] = temp_value and temp_value + REDd[t] or REDd[t]

            D = D + 1  # 统计文档数
        '''
        全局统计量计算
        '''
        TFc = TF(wordc)
        LEc, REc = Entropy(DTFc, termc)
        for t in termc:
            temp_value = IDF.get(w)
            temp = log(0.01 + D / DF[t], 2)
            IDF[t] = temp_value and temp_value + temp or temp
            '''
            平均左右信息熵计算
            '''
            LEDM[t] = LEDM[t] / DF[t]
            REDM[t] = REDM[t] / DF[t]

        '''
        文档标记
        '''
        index = 0
        w_pre = ''
        for w in wordc:  # 不知道存在不同的文档时，这样直接拉通索引科学不
            result[index][3] = LEc[w]  # 左信息熵
            result[index][4] = REc[w]  # 右信息熵
            result[index][5] = TFc[w]  # 全文词频
            result[index][6] = IDF[w]  # IDF
            result[index][7] = DTFc[(w_pre, w)]  # IFA
            result[index][11] = LEDM[t]  # 平均左信息熵
            result[index][12] = REDM[t]  # 平均右信息熵
            w_pre = w
            index = index + 1

        '''
        标记文档输出
        '''

    finally:
        if f1:
            f1.close()
