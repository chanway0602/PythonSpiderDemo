# -*- coding: utf-8 -*-

"本程序获取微博个人主页信息，保存cookie登陆"

from fake_useragent import UserAgent
from lxml import etree
import requests

class WeiboSpider(object):

    def __init__(self):
        self.url_1 = 'https://weibo.com/ajax/profile/info?uid=5537710542' # 此链接获取的是数据包json信息
        self.url_2 = 'https://weibo.com/u/5537710542' #此链接获取的是html文本信息
        self.headers = {
            #'User-Agent':UserAgent().random,
            # 注意，useragent最好不改变，否则cookie失效
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36', 
            # 将拷贝的cookie值放在此处
            'cookie':'_s_tentry=passport.weibo.com; Apache=626410993386.9077.1652760423368; SINAGLOBAL=626410993386.9077.1652760423368; \
            ULV=1652760423380:1:1:1:626410993386.9077.1652760423368:; login_sid_t=918920ae0b8ddc7bb233a7f4ed8b0830; cross_origin_proto=SSL; \
            _ga=GA1.2.1846765766.1652776910; _gid=GA1.2.1827856163.1652776910; wb_view_log=1920*10801; UOR=,,www.baidu.com; PC_TOKEN=9e58310aa9; \
            SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWuxgnZ_KysIbzTNM0TMRbm5JpX5o275NHD95QfSKeNS027SKBEWs4DqcjzBcyydLUywCXt; SSOLoginState=1652777186; \
            SUB=_2A25PhxCyDeRhGeNL6FUW8S7Jzz6IHXVs9QV6rDV8PUNbmtB-LXKkkW9NSQRYPwHAoH9cu_NSQuambdf1xrTG7jVd; ALF=1684313179; XSRF-TOKEN=6mT_eX5jb6sC_yofgCIsRyFR; \
            WBPSESS=iwj7SGZ1L56W_y9fTfwYjcD5xUCSy9M71V-HX0cpFsf7_aETLXjTDZ5YZfu_Uk9iL_Szm_U7MtNYNok3yXi0BcSb69-_caXow_Msy0F8d49GPxNBgrmJwSvO88ZivOsbxiuvEUyoXNP3yP8tpdeWeg=='
        }
        print(self.headers['User-Agent'])

    def run(self):
        # 获取html文本信息
        html = requests.get(url=self.url_2, headers=self.headers).text
        print(html)
        print('\n')

        # 获取数据包json信息
        content = requests.get(url=self.url_1, headers=self.headers).json()
        print(content)
        print('screen_name:{}'.format(content['data']['user']['screen_name']))
        print('location:{}'.format(content['data']['user']['location']))
        print('followers:{}'.format(content['data']['user']['followers_count']))
        print('friends:{}'.format(content['data']['user']['friends_count']))


def main():
    spider = WeiboSpider()
    spider.run()

if __name__ == '__main__':
    main()



