
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
        for i in range(150):
            url = "http://www.hnggzy.com/hnsggzy/jyxx/002001/002001001/?Paging=" + str(i)
            urls.append(url)
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        try:
            data = requests.get(url)
            data.encoding = 'gb2312'
            data = data.text
        except:
            return self.attr.DONE
        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", style="height:530px;")
        for tr_tag in div_tag.find_all("tr"):
            url_n="http://www.hnggzy.com" + tr_tag.find("a")["href"]
            date=tr_tag.find_all("td")[2].text[1:-1]
            result = self.url_increment.is_increment(url_n, date)
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'gb2312'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find_all("table", width="887")[0]
        title = table_tag.find_all("td", height="76")[0].get_text().strip().replace("\n", "")
        date = table_tag.find_all("td", height="30")[0].get_text().strip().replace("\n", "")[10:19]
        text = table_tag.find_all("td", style="padding:26px 40px 10px;")[0].get_text().strip()
        text = "".join(text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

if __name__ == '__main__':
    j = job.Job("cnpiec_16")
    j.submit("first","second","thrid",pyname="cnpiec_16")

