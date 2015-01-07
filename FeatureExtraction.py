#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 hanwei <hanwei20082123@163.com>


import os
from os.path import join
import sys
import chardet
import jieba
import jieba.posseg as pseg

jieba.enable_parallel(6)

top_path = u"清水河畔"

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')    #python2.7是基于ascii去处理字符流，当字符流不属于ascii范围内，就会抛出异常（ordinal not in range(128)）。
    try:
        f1 = open('./temp1', 'w')
        for novel in os.listdir(top_path):
            with open(join(top_path, novel)) as f:
                str_for_dect = f.read(1024)
                encoding = chardet.detect(str_for_dect)['encoding']
                f.seek(0)
                temp = f.read().decode(encoding, 'ignore')
                words = pseg.cut(temp)
                for w in words:
                    f1.write(w.word)
                    f1.write(u'\t')
                    f1.write(w.flag)
                    f1.write(u'\n')
    finally:
        if f1:
            f1.close()