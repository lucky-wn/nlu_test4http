# coding: utf-8
"""
@author: wangn8
@file: make.py
@time: 2021/10/27 19:55
"""
with open("input.txt", "r", encoding="utf8") as f:
    lines = f.readlines()
conts = list(set(lines))
conts.sort()
ret = open("./result.txt", "w", encoding="utf8")
for cts in conts:
    ret.write(cts)
ret.close()