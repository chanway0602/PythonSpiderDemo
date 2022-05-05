# coding=utf-8

'''
这是一个爬取特定网页html的代码demo，采用函数式编程

步骤如下：
1.导入所需模块
2.拼接url地址
3.向url发送请求
4.保存为本地文件
'''


#1.导入urllib库相关模块
from urllib import request
from urllib import parse

#2.拼接url地址
def make_url(word):
    url = 'https://www.baidu.com/s?'
    params = parse.urlencode({'wd':word})
    url = url + params
    return url

#3.向url发送请求
def request_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    return html

#4.保存为本地文件
def write_file(filename, html):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

#运行主程序
def main():
    word = input('请输入要搜索的内容\n')
    url = make_url(word)
    html = request_url(url)
    write_file('Chanway', html)

if __name__ == '__main__':
    main()
















