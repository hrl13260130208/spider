
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.job as job
import time
import re


class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        urls.append("http://ecp.cnnc.com.cn/xzbgg/index.jhtml")
        for i in range(349):
            urls.append("http://ecp.cnnc.com.cn/xzbgg/index_"+str(i+2)+".jhtml")
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        data = requests.get(url)
        data.encoding = "UTF-8"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="List1")

        for li in div_tag.find_all("li"):
            a = li.find("a")["href"]
            url_n= "http://ecp.cnnc.com.cn" + a
            date = li.find("span", class_="Right Gray").text
            result=self.url_increment.is_increment(url_n,date)
            if result:
                urls.append(url_n)
        return urls


class thrid(ss.ThreadingSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "UTF-8"
        data = resq.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="W980 Center PaddingTop10")
        title = div_tag.find("h1").text.strip()

        div_tag2 = div_tag.find("div", class_="Padding10 TxtCenter Gray").text.strip()
        s_num = div_tag2.find("发布时间：")
        e_num = div_tag2.find("浏览次数：")
        dt = div_tag2[s_num + 5:e_num].strip()
        date = dt.split(" ")[0]
        start = data.find('<div class="Contnet" style="min-height:500px; padding:0 30px;">')
        end = data.find('<ul style="text-align:center; padding:10px;">')
        text = data[start:end]
        p = re.compile('(?<=\>).*?(?=\<)')
        result = p.findall(text)
        text = "".join(result)
        line = url + "##" + date + "##" + title + "##" + text+"\n"
        return line

if __name__ == '__main__':
    j = job.Job("cnpiec_47")
    j.submit("first","second","thrid",pyname="cnpiec_47")

