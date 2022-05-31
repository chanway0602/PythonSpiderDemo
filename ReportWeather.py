# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests

class WeatherSpider(object):
    def __init__(self):
        self.url = 'https://restapi.amap.com/v3/weather/weatherInfo?' # 使用高德天气API
        self.headers = {
            'User-Agent':UserAgent().random
        }
        self.params = {
            'key':'7093990e62af2f0e095c4b5a5be41cbe', # 请求服务权限标识
            'city':'440300',# 城市编码
            'extensions':'all',# 气象类型,可选值：base/all,base:返回实况天气,all:返回预报天气
            'output': 'JSON'# 返回格式,可选值：JSON,XML
        }

    def parse(self):
        res = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        #print(res)
        if res['status'] == '1': # 返回状态,1：成功；0：失败
            forecasts = res['forecasts'][0]
            weather = forecasts['province'] + forecasts['city'] + forecasts['casts'][0]['date'] + '\n' + \
                      '白天天气：' + forecasts['casts'][0]['dayweather'] + ' 气温：' + forecasts['casts'][0]['daytemp'] + '\n' + \
                      '晚上天气：' + forecasts['casts'][0]['nightweather'] + ' 气温：' + forecasts['casts'][0]['nighttemp']
            return weather
        else:
            print('request failed')
            return

class PushDeer(object):
    def __init__(self, text, type):
        self.url = 'https://api2.pushdeer.com/message/push'
        self.headers = {
            'User-Agent':UserAgent().random
        }
        self.params = {
            'pushkey':'PDU9345TUh0hLQk42msCMH7iCOSbPdHwMY3CN9VP', # iphone12
            'text':text,
            'type':type
        }

    def pushdevice(self):
        requests.get(url=self.url, params=self.params, headers=self.headers)

def main():
    spider = WeatherSpider()
    weather = spider.parse()

    deer = PushDeer(weather, None)
    deer.pushdevice()

if __name__ == '__main__':
    main()

