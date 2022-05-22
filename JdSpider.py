# -*- coding: utf-8 -*-

"""
本程序目标:抓取京东商城(https://www.jd.com/)商品名称、商品价格、评论数量,以及商铺名称。比如输入搜索“Python书籍”,则抓取如下数据:
{'name': 'Python编程 从入门到实践 第2版 人民邮电出版社', 'price': '￥52.50', 'count': '200+条评价', 'shop': '智囊图书专营店'}
{'name': 'Python编程 从入门到实践 第2版(图灵出品)', 'price': '￥62.10', 'count': '20万+条评价', 'shop': '人民邮电出版社'}
...
"""

from selenium import webdriver
import time

class JdSpier(object):

    def __init__(self):
        self.url = 'https://www.jd.com/' #京东网站主页

    def search_item(self):
        """
        options=webdriver.ChromeOptions() # 无头模式，不用打开浏览器，提升速度
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        """
        driver = webdriver.Chrome()
        #driver.maximize_window() #最大化窗口

        driver.get(self.url)
        driver.find_element_by_xpath('//*[@id="key"]').send_keys('python书籍') #在搜索框内输入书籍            参考路径 //*[@id="key"]
        driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click() #找到‘搜索’按钮并点击     参考路径 //*[@class='form']/button
        time.sleep(2) #等待2s出页面

        while True:
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') #执行js代码，滑到页面最下方
            time.sleep(2) #等待2s出页面

            page_end = driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[@class="p-num"]/a[9]') 
            if page_end.get_attribute('class') == 'pn-next': #pn-next disabled
            #if self.browser.page_source.find('pn-next disabled')==-1: #另一种判断方式，全页查找
                item_list = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li') #获取商品xpath的list
                self.save_item(item_list)
                driver.find_element_by_class_name('pn-next').click()
                time.sleep(2)
            else:
                break

        time.sleep(10) #等待10s
        driver.quit()
        
    def save_item(self, item_list):
        item = {}
        for i in item_list: 
            item['name']  = i.find_element_by_xpath('.//div/a/em').text.strip()     #参考路径 .//div[@class="p-name"]/a/em
            item['price'] = i.find_element_by_xpath('.//div/strong/i').text.strip() #参考路径 .//div[@class="p-price"]
            item['count'] = i.find_element_by_xpath('.//div/strong/a').text.strip() #参考路径 .//div[@class="p-commit"]/strong
            item['shop']  = i.find_element_by_xpath('.//div/div[@class="p-shopnum"]').text.strip() #参考路径 .//div[@class="p-shopnum"]
            print(item)

def main():
    spider = JdSpier()
    spider.search_item()
    

if __name__ == '__main__':
    main()
