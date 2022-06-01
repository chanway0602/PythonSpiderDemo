# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import logging

logging.basicConfig(level=logging.INFO, 
                    filename='/root/workspace/logs/ReportWeather.log',
                    filemode='a+',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
"""
#use logging:
logging.info('这是 loggging info message')
logging.debug('这是 loggging debug message')
logging.warning('这是 loggging warning message')
logging.error('这是 loggging error message')
logging.critical('这是 loggging critical message')
"""

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
        #logging.info(res)
        if res['status'] == '1': # 返回状态,1：成功；0：失败
            forecasts = res['forecasts'][0]
            weather = forecasts['province'] + forecasts['city'] + forecasts['casts'][0]['date'] + '\n' + \
                      '白天天气：' + forecasts['casts'][0]['dayweather'] + ' 气温：' + forecasts['casts'][0]['daytemp'] + '\n' + \
                      '晚上天气：' + forecasts['casts'][0]['nightweather'] + ' 气温：' + forecasts['casts'][0]['nighttemp']
            logging.info(weather)
            return weather
        else:
            logging.error('request failed')
            return

class PushDeer(object):
    def __init__(self, text, type):
        self.url = 'https://api2.pushdeer.com/message/push' # PushDeer url
        self.headers = {
            'User-Agent':UserAgent().random
        }
        self.params = {
            'pushkey':'PDU9345TUh0hLQk42msCMH7iCOSbPdHwMY3CN9VP', # iphone12
            'text':text, # 文本内容，若type为image，text为url
            'type':type  # text类型，文本为None，图片为image
        }

    def pushdevice(self):
        requests.get(url=self.url, params=self.params, headers=self.headers) # 推送到设备
        logging.warning('push finished')

def main():
    spider = WeatherSpider()
    weather = spider.parse()

    deer = PushDeer(weather, None)
    deer.pushdevice()

if __name__ == '__main__':
    main()

