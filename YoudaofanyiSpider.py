# -*- coding: utf-8 -*-

"""
本程序利用网络抓包,实现对有道翻译(https://fanyi.youdao.com/)的破解
"""

"""
有道网站:https://fanyi.youdao.com/

请求头信息：
Request URL: https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
Request Method: POST

数据包信息:(变化量:i, salt, sign, lts)
From Data:{
i: hello world
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 16526859055613
sign: 934f424d55c5c558bd5798e067244cf2
lts: 1652685905561
bv: a6a7eab4afbf9b019ca15a461e45e966
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTlME}

salt, sign的JS代码:
var r = function(e) {
    var t = n.md5(navigator.appVersion),
    r = "" + (new Date).getTime(),
    i = r + parseInt(10 * Math.random(), 10);
    return {
        ts: r,
        bv: t,
        salt: i,
        sign: n.md5("fanyideskweb" + e + i + "Tbh5E8=q6U3EXe+&L[4c@")
    }
};

对应关系: lts:r, salt:i, sign:sign 
"""

from hashlib import md5
import random
from time import time
import requests
from fake_useragent import UserAgent


class YoudaoSpider(object):

    # 初始化
    def __init__(self):
        # 通用的，基本不变的类变量
        # https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
        self.url = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule' # '_o'是为反爬加的字串，需要去掉
        self.headers = {'User-Agent':UserAgent().random}

    # 制作请求数据
    def make_data(self, word):
        lts  = str(int(time() * 1000)) # 13位, 乘1000, 取整
        salt = lts + str(random.randint(0, 9)) # 14位, lts加上0-9的随机数

        s = "fanyideskweb" + word + str(salt) + "Tbh5E8=q6U3EXe+&L[4c@"
        sign = md5() # 实例md5对象
        sign.update(s.encode()) # 调用前要对s字串进行编码，否则会报错

        #print(lts)
        #print(salt)
        #print(sign.hexdigest())

        return lts, salt, sign.hexdigest()

    # 获取请求结果
    def get_result(self, word):
        lts, salt, sign = self.make_data(word)

        # 请求的数据
        data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': lts,
            'bv': 'a6a7eab4afbf9b019ca15a461e45e966',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME' ,
        }

        res = requests.post(url=self.url, data=data, headers=self.headers)
        #print(res.text.strip()) # 返回的是json字串

        result = res.json()['translateResult'][0][0]['tgt'] # res.json() 将json格式的字符串转为python数据类型
        print('翻译结果:{}'.format(result)) 

        return result
        
    def run(self):
        try:
            word = input('请输入要翻译的内容\n')
            self.get_result(word)    
        except Exception as e:
            print(e)

def main():
    spider = YoudaoSpider()
    spider.run()

if __name__ == "__main__":
    main()
