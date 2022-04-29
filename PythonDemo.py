# coding=utf-8

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



try:
    with open(os.path.join(dirpath, 'spider.py'), 'rb+') as file:
        file.write(b'111')

except Exception as e:
        print(e)



