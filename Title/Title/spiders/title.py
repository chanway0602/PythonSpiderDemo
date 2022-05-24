import scrapy
class TitleSpider(scrapy.Spider):
    name = 'title'
    #要抓取数据的网站域名
    allowed_domains = ['c.biancheng.net']
    #第一个抓取的url，初始url,被当做队列来处理
    start_urls = ['http://c.biancheng.net/']
    
    def parse(self,response):
        #.extract()：提取文本内容,将列表中所有元素序列化为Unicode字符串
        #.extract_first()：提取列表中第1个文本内容
        # 以下是我们自己编写的代码，而自动生成的代码不用改动
        result = response.xpath('/html/head/title/text()').extract_first()
        print('-' * 60 )
        print(result)
        print('-' * 60)

        