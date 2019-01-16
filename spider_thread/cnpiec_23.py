
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.job as job
import time
import random
import re




class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        for i in range(3081):
            if i == 0:
                continue
            url = "http://www.jxsggzy.cn/web/jyxx/002006/002006001/" + str(i) + ".html"
            urls.append(url)
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        try:
            data = requests.get(url)
        except:
            return self.attr.DONE
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag=soup.find("div", class_="ewb-infolist")
        for li_tag in div_tag.find_all("li"):
            a_tag=li_tag.find("a")
            url_n="http://www.jxsggzy.cn" + a_tag["href"]
            date = li_tag.find("span").text
            print(url_n, date)
            result = self.url_increment.is_increment(url_n, date)
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div = soup.find_all("div", class_="article-info")[0]
        [s.extract() for s in div('script')]
        [s.extract() for s in div('style')]
        title = div.find_all("h1")[0].get_text().strip().replace("\n", "")
        date = div.find_all("p", class_="infotime")[0].get_text().strip().replace("\n", "")
        text = div.find_all("div")[0].get_text().strip()
        text = "".join(text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

if __name__ == '__main__':
    j = job.Job("cnpiec_23")
    j.submit("first","second","thrid",pyname="cnpiec_23")

