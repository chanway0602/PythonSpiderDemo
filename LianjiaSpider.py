# -*- coding: utf-8 -*-

"""
本节使用 Python 爬虫库完成链家二手房（https://bj.lianjia.com/ershoufang/rs/）房源信息抓取，包括楼层、区域、总价、单价等信息。
html解析使用xpath

https://bj.lianjia.com/ershoufang/pg{n}/
"""

import requests, csv
from fake_useragent import UserAgent
from lxml import etree

class LianjiaSpider(object):

    # 初始化
    def __init__(self) :

        # 初始化一个ua
        ua = UserAgent()

        self.url = 'https://bj.lianjia.com/ershoufang/pg{}/'
        # 使用随机的ua
        self.headers = {'User-Agent':ua.random}

        '''
        /html/body/div[4]/div[1]/ul/li[2]
        /html/body/div[@id='content']/div[@class='leftContent']/ul[@class='sellListContent']/li[@class='clear LOGCLICKDATA'][1]/div[@class='info clear']/div[@class='title']/a
        '''
        self.p_xpath = '/html/body/div[4]/div[1]/ul/li'  # F12定位输出的xpath绝对路径
        #self.p_xpath = '//*[@id="content"]/div[1]/ul/li' # F12定位输出的xpath相对路径  
        #self.p_xpath = '//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]' # xpath helper输出的路径，注意@class属性有触发事件
        self.title_xpath = './/div[@class="info clear"]/div[@class="title"]/a/text()'
        self.locationinfo_xpath = './/div[@class="flood"]/div[@class="positionInfo"]/a/text()'
        self.houseinfo_xpath = './/div[@class="address"]/div[@class="houseInfo"]/text()'
        self.priceinfo_xpath = './/div[@class="priceInfo"]/div[@class="totalPrice totalPrice2"]/span/text()'

    # 获取html
    def get_html(self, url):

        html  = requests.get(url=url, headers=self.headers).text
        #print(html)

        return html

    # 解析html
    def parse_html(self, html):

        # 获得一个html的xpath对象
        p_html = etree.HTML(html)
        # 获取指定的xpath list
        p_list = p_html.xpath(self.p_xpath)
        #print(p_list)
        
        item = {}
        for p in p_list:
            # 芍药居北里 满五年南北向 有客厅 诚心出售
            title_list = p.xpath(self.title_xpath)
            item['title'] = title_list[0].strip() if title_list else None

            # 芍药居北里 - 芍药居
            location_list = p.xpath(self.locationinfo_xpath)
            item['location'] = location_list[0].strip() if location_list else None

            # 539
            price_list = p.xpath(self.priceinfo_xpath)
            item['price'] = price_list[0].strip() + '万' if price_list else None

            # 2室1厅 | 57.8平米 | 南 北 | 精装 | 中楼层(共7层) | 板楼
            houseinfo_list = p.xpath(self.houseinfo_xpath)
            if houseinfo_list:
                L = houseinfo_list[0].split('|')
                if len(L) >= 6:
                    item['model']    = L[0].strip()
                    item['area']     = L[1].strip()
                    item['direct']   = L[2].strip()
                    item['perfect']  = L[3].strip()
                    item['floor']    = L[4].strip()
                    item['type']     = L[5].strip()

            print(item)
            self.save_info(item)  
        
        return item

    # 保存信息
    def save_info(self, item):

        fieldnames = item.keys() #构建字段名
        with open('Lianjia.csv', 'a', newline='') as csvfile:
            spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            spamwriter.writeheader() # 写入字段名，当做表头
            spamwriter.writerow(item) # 单行写入

    # 运行
    def run(self):

        url = self.url.format('1')
        html = self.get_html(url)
        item_list = self.parse_html(html)


# 主函数
def main():
    spider = LianjiaSpider()
    spider.run()

if __name__ == '__main__':
    main()
