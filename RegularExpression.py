# coding=utf-8

import re


website="编程帮 www.biancheng.net"


pattern = re.compile(r'(.*?)\s+(.*)', re.S)
str = pattern.findall(website)
print(str)
for i in str:
    print(i[0])
    print(i[1])
print(30*'*'+'\n')

html="""
<div class="movie-item-info">
<p class="name">
<a title="你好，李焕英">你好，李焕英</a>
</p>
<p class="star">
主演：贾玲,张小斐,沈腾
</p>    
</div>
<div class="movie-item-info">
<p class="name">
<a title="刺杀，小说家">刺杀，小说家</a>
</p>
<p class="star">
主演：雷佳音,杨幂,董子健,于和伟
</p>    
</div> 
"""

pattern = re.compile(r'<div.*?<a title="(.*?)".*?"star">(.*?)</p.*?div>', re.S)
str = pattern.findall(html)
print(str)
for i in str:
    print('电影名称:{}'.format(i[0].strip()))
    print('演员名单:{}'.format(i[1].strip()))








