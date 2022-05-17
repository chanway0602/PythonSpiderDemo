# -*- coding: utf-8 -*-

"""
本节实现抓取豆瓣电影“分类排行榜”中的电影数据(https://movie.douban.com/chart),比如输入“犯罪”则会输出所有犯罪影片的电影名称、评分，效果如下所示：
剧情|喜剧|动作|爱情|科幻|动画|悬疑|惊悚|恐怖|纪录片|短片|情色|同性|音乐|歌舞|家庭|儿童|传记|历史|战争|犯罪|西部|奇幻|冒险|灾难|武侠|古装|运动|黑色电影|
你想了解什么类型电影:犯罪
{'name': '肖申克的救赎', 'score': 9.7}
{'name': '控方证人', 'score': 9.6}
...
电影总数量:302部
"""

"""
设计思路：
1. 一级页面 https://movie.douban.com/chart 是静态页面，可获取类型对应的type num，如：<span><a href="/typerank?type_name=剧情&type=11&interval_id=100:90&action=">剧情</a></span>
   作为后面访问动态页面的参数。

2. 点击“剧情”，会跳转到二级动态页面，抓包发现，请求url为：https://movie.douban.com/j/chart/top_list?type=11&interval_id=100:90&action=&start=20&limit=20
   请求方式为：GET
   请求信息为：
        type: 11 #影片类型
        interval_id: 100:90 #好于100%-90%的...
        action: #空
        start: 20 #页数，n*20
        limit: 20 #定值
    滚动观察发现，只有start会改变，其他都是定值。

3. 抓包查看其他异步信息，可得到影片数量：{"playable_count":503,"total":814,"unwatched_count":814} #可播放；影片总数；未观看数
"""

from fake_useragent import UserAgent
import requests, re

class DoubanchatSpiser(object):

    # 初始化
    def __init__(self):
        self.headers = {'User-Agent':UserAgent().random}
        self.url_one = 'https://movie.douban.com/chart'
        self.url_two = 'https://movie.douban.com/j/chart/top_list?'  
        self.url_count = 'https://movie.douban.com/j/chart/top_list_count?'

    # 获取一级页面的类型菜单，和对应的类型号
    def get_menu(self):
        html = requests.get(url=self.url_one, headers=self.headers).text

        reg  = r'<span><a href=.*?type_name=(.*?)&type=(.*?)&interval_id.*?</span>'
        pattern = re.compile(reg, re.S)
        menu_list = pattern.findall(html)

        item = {}
        for group in menu_list:
            item[group[0].strip()] = group[1].strip()

        #print(item)
        return item

    def get_film_count(self, filmtype):
        item = self.get_menu()
        type_num = item[filmtype]
        params = {
            'type': type_num,
            'interval_id': '100:90'
        }
        res = requests.get(url=self.url_count, params=params, headers=self.headers).json()

        return res['total']

    def get_film_total(self, filmtype):
        item = self.get_menu()
        type_num = item[filmtype]
        total_count = self.get_film_count(filmtype)
        print('{}类型的电影总共有{}部'.format(filmtype, total_count))

        total_film = {}
        for page in range(0, total_count, 20):
            #print(page)
            params = {
                'type': type_num, #影片类型
                'interval_id': '100:90', #好于100%-90%的...
                'action': '',#空
                'start': str(page), #页数，n*20
                'limit': '20' #定值          
            }
            res_list = requests.get(url=self.url_two, params=params, headers=self.headers).json()
            for res in res_list:
                total_film['name'] = res['title'].strip()
                total_film['regions']  = res['regions'][0].strip()
                total_film['score']    = res['score'].strip()    
                print(total_film)
        
            print('第{}页爬取成功！'.format(page/20+1))
    
    def run(self):
        item = self.get_menu()
        print(item.keys())
        filmtype = input('请输入你要查询的电影类型:\n')
        self.get_film_total(filmtype)

    
def main():
    spider = DoubanchatSpiser()
    spider.run()


if __name__ == '__main__':
    main()    
        





