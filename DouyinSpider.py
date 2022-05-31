# -*- coding: utf-8 -*-

"""
目标功能：本程序检测抖音博主主页视频，有更新即下载保存。
已实现功能：根据短链下载主页全部视频
"""

"""
分析过程：
author: 俄罗斯[进口馆]
短链: https://v.douyin.com/Fgv6Nee/
https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAA8FpIYfAOBc-b9KgE5Mwog1Q0KVRTi6Bm4qTy2nqMlcg&count=21&max_cursor=0&_signature=1u.u6wAAtGybK8bXaxHkpNbv7v

author:思维格局（王老师）
短链: https://v.douyin.com/FHobMX8/
https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAI4aF4DJ3P9MrmT_TpC7dNTK7sQ4EsTYdLkbZJmHlm5q7ClPZvmgDDsSOccGcMUxA&count=21&max_cursor=0&_signature=3yESUQAAvbiS5TptvGOkVN8hEk
https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAI4aF4DJ3P9MrmT_TpC7dNTK7sQ4EsTYdLkbZJmHlm5q7ClPZvmgDDsSOccGcMUxA&count=21&max_cursor=1652683605000&_signature=3yESUQAAvbiS5TptvGOkVN8hEk
https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAAI4aF4DJ3P9MrmT_TpC7dNTK7sQ4EsTYdLkbZJmHlm5q7ClPZvmgDDsSOccGcMUxA&count=21&max_cursor=1652577734000&_signature=3yESUQAAvbiS5TptvGOkVN8hEk

url:
    https://www.iesdouyin.com/web/api/v2/aweme/post/
params:
    sec_uid
    count = 21
    max_cursor
    _signature

"""

import requests, re, os
from fake_useragent import UserAgent

class DouyinSpider(object):

    # 初始函数
    def __init__(self):
        self.url = 'https://v.douyin.com/Fv7sumE/' # 博主主页分享的短链接
        self.headers = {'User-Agent':UserAgent().random}
        #self.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Mobile Safari/537.36'}
        
        res = requests.head(url=self.url, headers=self.headers) #head请求
        sec_uid = re.findall(r'sec_uid=(.*?)&', res.headers['location'], re.S)[0] #从location信息中获取sec_uid

        self.params = {
            'sec_uid':sec_uid, # 固定值
            'count'  :'21', # 固定是21
            'max_cursor':'0', # 这个参数第一个包的值是0,后续的值由其上一个包的值决定
            '_signature':'VPvcPQAANm4ZP.QBZsaaT1T73C' # 这个是签名请求参数，由于尚未破解，需要手动获取
        }
        print(self.params)

    # 获取博主信息
    def get_authorinfo(self):
        user_info_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=' + self.params['sec_uid']
        res = requests.get(url=user_info_url, headers=self.headers).json()
        self.user_info = {
            'nickname':res.get('user_info').get('nickname').strip(), # 名称
            'following_count':res.get('user_info').get('following_count'), # 关注数
            'follower_count' :res.get('user_info').get('follower_count'), # 粉丝数
            'aweme_count' :res.get('user_info').get('aweme_count'), # 作品数
            'signature' :res.get('user_info').get('signature').strip(), # 签名
            'uid' :res.get('user_info').get('uid'), # uid
            'unique_id' :res.get('user_info').get('unique_id'), # 抖音号
        }
        print(self.user_info)

    # 解析, 下载视频
    def parse_packet(self):
        user_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/' # 请求包的基地址

        count = 0 # 记录包的请求次数
        while True:
            res = requests.get(url=user_post_url, headers=self.headers, params=self.params).json()
            aweme_list = res.get('aweme_list')
            if aweme_list:
                count = 0 # 记数清零
                for aweme in aweme_list:
                    desc = aweme['desc'].strip() # 标题描述
                    aweme_id = aweme['aweme_id'].strip() # aweme_id
                    video_url_list = aweme['video']['play_addr']['url_list'] # 视频下载链接列表，共4个，前面两个不能播放，后面两个可以播放
                    self.params['max_cursor'] = res.get('max_cursor') # 记录max_cursor作为下一个包的requests参数
                    self.download_video(aweme_id + desc, video_url_list[2]) # 取第三个链接地址

            elif not aweme_list and count < 5: # 若aweme_list为空，可能是网络问题，循环请求五次
                count += 1 # 记数+1
                continue

            else: # 抓取完毕
                print('{}主页视频抓取完毕'.format(self.user_info['nickname']))
                break
            
    # 下载视频
    def download_video(self, desc, url):
        if not os.path.exists(self.user_info['nickname']): # 以主页名新建文件夹
            os.mkdir(self.user_info['nickname'])

        file_dir = os.path.abspath(self.user_info['nickname'])
        file_path = os.path.join(file_dir, desc + '.mp4') #以 aweme_id+desc命名mp4文件
        content = requests.get(url=url, headers=self.headers).content #获取视频内容
        print('开始下载:' + file_path)
        with open(file_path, 'wb') as f:
            f.write(content)
        print('下载完成:' + file_path)

def main():
    spider = DouyinSpider()
    spider.get_authorinfo()
    spider.parse_packet()

if __name__ == '__main__':
    main()

