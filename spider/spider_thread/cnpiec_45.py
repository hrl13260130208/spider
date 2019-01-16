
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
        for i in range(150):
            urls.append("http://new.zmctc.com/zjgcjy/jyxx/004001/004001001/?Paging="+str(i+1))
            urls.append("http://new.zmctc.com/zjgcjy/jyxx/004001/004001002/?Paging="+str(i+1))
            urls.append("http://new.zmctc.com/zjgcjy/jyxx/004001/004001003/?Paging="+str(i+1))
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        header = {"User-Agent":
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        try:
            data = requests.get(url, headers=header)
            data.encoding = "UTF-8"
            data = data.text
        except:
            return self.attr.DONE
        soup = BeautifulSoup(data, "html.parser")
        div = soup.find("div", align="center")
        for tr_tag in div.find_all("tr", height="30"):
            a = tr_tag.find("a")
            url_n = "http://new.zmctc.com" + a["href"]
            date = tr_tag.find("td", width="80").text
            result = self.url_increment.is_increment(url_n, date[1:-1])
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        resq = requests.get(url, headers=header)
        resq.encoding = "UTF-8"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        table_tag = soup.find("table", id="tblInfo")
        td_tag = table_tag.find("td", id="tdTitle")
        t_font = td_tag.find("font", style="font-size: 25px")
        d_font = td_tag.find("font", class_="webfont")
        title = t_font.text.strip()
        d_line = d_font.text.strip()
        end = d_line.find("】")
        date = d_line[6:end].strip().replace("/", "-")
        text = "".join(table_tag.text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

def test():
    urls = []
    url="http://new.zmctc.com/zjgcjy/jyxx/004001/004001001/?Paging=1"
    header={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    data = requests.get(url,headers=header)
    data.encoding = "UTF-8"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    div=soup.find("div",align="center")
    for tr_tag in div.find_all("tr",height="30"):
        a=tr_tag.find("a")
        url_n="http://new.zmctc.com"+a["href"]
        date=tr_tag.find("td",width="80").text
        print(url_n,date[1:-2])

    return urls





def test2():
    url="http://new.zmctc.com/zjgcjy/InfoDetail/?InfoID=9329daf9-0310-4ded-bee7-3dd6fca0ae35&CategoryNum=004001001"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    resq=requests.get(url,headers=header)
    resq.encoding = "UTF-8"
    data=resq.text
    soup=BeautifulSoup(data,"html.parser")
    # [s.extract() for s in soup("style")]
    # print(soup.text)
    table_tag=soup.find("table",id="tblInfo")
    td_tag=table_tag.find("td",id="tdTitle")
    t_font=td_tag.find("font",style="font-size: 25px")
    d_font=td_tag.find("font",class_="webfont")
    title=t_font.text.strip()
    d_line=d_font.text.strip()
    end=d_line.find("】")
    date=d_line[6:end].strip().replace("/","-")
    text="".join(table_tag.text.split())
    line = url + "##" + date + "##" + title + "##" + text + "\n"
    return line






if __name__ == '__main__':
    j = job.Job("cnpiec_45")
    j.submit("first","second","thrid",pyname="cnpiec_45")

