# -*- coding: utf-8 -*-

from fileinput import filename
from importlib.resources import path
import logging
from re import X
from unicodedata import name


def Demo():
    xxx = 0
    if xxx is not None:
        ...
    elif 0:
        ...
    else:
        ...


x = [a * a if a > 5 else -1 for a in range(1,11)] #
y = [a * a for a in range(1, 11) if a > 5]
z = (a * a for a in range(1, 11)) #z is a generator, take value with func next
print(x)
print(y)
'''
for a in list(z):
    print(a)
'''


import sys

from selenium import webdriver
import logging


class Student(object):
    
    def __init__(self, name, score):
        self.name  = name
        self.score = score

    def show(self):
        print('name:%s, score:%d' % (self.name, self.score))


A = Student('John', 90)
A.show()

B = Student('Lucika', 100)
B.show()

print(9%4)

import os
filepath = os.path.abspath(__file__)
#print(os.path.abspath(__file__))

dirpath  = os.path.split(filepath)[0]
filename = os.path.split(filepath)[1]

print(dirpath, filename)
spiderpath = os.path.join(dirpath, 'spider.py')
print(spiderpath)


'''
try:
    with open(os.path.join(dirpath, 'spider.py'), 'rb+') as file:
        file.write(b'111')

except Exception as e:
        print(e)
'''


#字符串拼接的三种方式
#1.直接字符串相加：
xxx = '111' + '222'

#2.使用format函数：
yyy = 'this is {} {}'.format('demo', '2')

#3.格式化拼接：
zzz = 'Python No.%s' % '1'


print('\n')

import requests
url = 'https://img0.baidu.com/it/u=908725181,3965400702&fm=253&fmt=auto&app=138&f=JPEG?w=496&h=440'
#url = 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=38785274,1357847304&fm=26&gp=0.jpg'
# 简单定义浏览器ua信息
headers = {'User-Agent':'Mozilla/4.0'}
# 读取图片需要使用content属性
html = requests.get(url=url,headers=headers).content
# 以二进制的方式下载图片
with open('python_logo.jpg','wb') as f:
    f.write(html)

item = {'website': 'C语言中文网', 'url': "c.biancheng.net"}
for k,v in item.items():
    print(k)
    print(v)


