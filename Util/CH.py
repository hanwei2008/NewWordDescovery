#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 hanwei <hanwei20082123@163.com>

'''
自己编写的一些中文字符操作
'''

def str_len(str):  
    try:  
        row_l=len(str)  
        utf8_l=len(str.encode('utf-8'))  
        return (utf8_l-row_l)/2+row_l  
    except:  
        return None  
    return None 