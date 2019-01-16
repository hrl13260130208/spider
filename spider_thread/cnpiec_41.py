
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.job as job
import time
import random
import json




class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        for i in range(50):
            urls.append("http://zbxx.ycit.cn/zbxx/Index.asp?page="+str(i+1))
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        try:
            data = requests.get(url)
            data.encoding = "gbk"
            data = data.text
        except:
            return self.attr.DONE
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", width="722", height="500")
        td = table_tag.find("td", width="722")
        table = td.find("table")
        for tr in table.find_all("tr"):
            a = tr.find("a", target="_self")
            date = tr.find("td", align="right")
            if a == None:
                continue
            url_n = "http://zbxx.ycit.cn" + a["href"]
            result = self.url_increment.is_increment(url_n, date.text.strip())
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "gbk"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", width="1004", height="462")
        td = table_tag.find("td", width="1000")
        table = td.find("table")
        title = table.find("td", class_="wzrr").text.strip()
        d_td = table.find("tr", align="middle").text.strip()
        start = d_td.find("更新时间：")
        date = d_td[start + 5:]
        text = "".join(table_tag.text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

def test():
    urls = []
    url="http://zbxx.ycit.cn/zbxx/Index.asp?page=1"
    data = requests.get(url)
    data.encoding = "gbk"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    table_tag=soup.find("table",width="722",height="500")
    td=table_tag.find("td",width="722")
    table=td.find("table")
    for tr in table.find_all("tr"):
        a=tr.find("a",target="_self")
        date=tr.find("td",align="right")
        if a==None:
            continue
        url_n="http://zbxx.ycit.cn"+a["href"]
        print(url_n,date.text.strip())

    return urls

def test2():
    url="http://zbxx.ycit.cn/zbxx/ShowArticle.asp?ArticleID=768"

    resq=requests.get(url)
    resq.encoding = "gbk"
    data=resq.text
    soup=BeautifulSoup(data,"html.parser")
    table_tag = soup.find("table", width="1004", height="462")
    td = table_tag.find("td", width="1000")
    table = td.find("table")
    title=table.find("td",class_="wzrr").text.strip()
    d_td=table.find("tr",align="middle").text.strip()
    start=d_td.find("更新时间：")
    date=d_td[start+5:]

    text="".join(table_tag.text.split())
    line = url + "##" + date + "##" + title + "##" + text + "\n"
    return line






if __name__ == '__main__':
    j = job.Job("cnpiec_41")
    j.submit("first","second","thrid",pyname="cnpiec_41")

