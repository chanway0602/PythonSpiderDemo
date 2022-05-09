# coding=utf-8

import csv
# 操作文件对象时，需要添加newline参数逐行写入，否则会出现空行现象
with open('eggs.csv', 'w', newline='') as csvfile:
    # delimiter 指定分隔符，默认为逗号，这里指定为空格
    # quotechar 表示引用符
    # writerow 单行写入，列表格式传入数据
    spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|')
    spamwriter.writerow(['www.biancheng.net'] * 5 + ['how are you'])
    spamwriter.writerow(['hello world', 'web site', 'www.biancheng.net'])
    

with open('eggs.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))
























