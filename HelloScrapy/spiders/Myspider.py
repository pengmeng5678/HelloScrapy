import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from pyquery import PyQuery as pq

from HelloScrapy.items import DingdianItem

class Myspider(scrapy.Spider):
    name = 'dingdian'#这个必须和entrypoint.py的第三个参数一致
    #allowed_domains，这个不是必须的，如果使用了爬取规则的时候就需要了
    #它的作用是只会跟进存在于allowedn_domains中的url，不存在的url会被忽略
    allowed_domains = ['23us.com']
    base_url = 'http://www.23us.com/class/'
    baseurl = '.html'

    def start_requests(self):
        for i in range(1,3):
            url = self.base_url+str(i)+'_1'+self.baseurl
            # yield Request(url,self.parse)   #这里讲返回的respons作为参数传递给self.parse，这个叫回调函数
            yield Request('http://www.23us.com/quanben/1',self.parse)

    #这个函数接收上门request获取到的response，不要轻易改写parse函数
    #因为这个函数被自己用了，就没谁接收request返回的response了，如果需要改，就需要自己定义一个新的回调函数
    def parse(self, response):
        # print('response:',response.text)
        #BeautifulSoup解析当前全本页面的所有url的html
        max_num = BeautifulSoup(response.text,'lxml').find('div',class_='pagelink').find_all('a')[-1].get_text()
        #取出 http://www.23us.com/quanben/
        bashurl = str(response.url)[:-1]
        print(max_num,bashurl)
        #for num in range(1,max_num+1):
        for num in range(1,3):
            url = bashurl+str(num)
            #自定义一个回调函数get_name，返回值以参数的形式传递给get_name函数
            yield Request(url,callback=self.get_name)

    def get_name(self,response):#解析单个页面文章列表中的文章名称和对应的文章url,如http://www.23us.com/quanben/
        # print('get_name',response)
        #这里返回一个td列表
        tds = BeautifulSoup(response.text,'lxml').find_all('tr',bgcolor='#FFFFFF')
        for td in tds:
            print('td:',td)
            novelname = td.find('a',target="_blank").get_text()
            novelurl = td.find('a',target="_blank")['href']
            author = td.find(class_="C").get_text()
            serialnumber = td.find(class_="R").get_text()
            # print('novelname,author,novelurl,word_count:',novelname,author,novelurl,word_count)
            #这里的meta是scrapy中传递额外数据的方法，因为我们还有一些其他内容需要再下一个页面才能获取到
            yield Request(novelurl,callback=self.get_chapterurl,meta={'name':novelname,'url':novelurl,'author':author,'serialnumber':serialnumber})

    def get_chapterurl(self,response):
        item = DingdianItem()
        item['category'] =  BeautifulSoup(response.text,'lxml').find(attrs = {"name": "og:novel:category"})['content']
        item['serialstatus'] =  BeautifulSoup(response.text,'lxml').find(attrs = {"name": "og:novel:status"})['content']
        item['name'] = str(response.meta['name']).replace('/xa0','')
        item['novelurl'] = str(response.meta['url'])
        item['author'] = str(response.meta['author'])
        item['serialnumber'] = str(response.meta['serialnumber'])
        print('category='+item['category'],'serialstatus='+item['serialstatus'],'name='+item['name'],'noveur='+item['novelurl'],'author='+item['author'],'serialnumber='+item['serialnumber'])
        yield item