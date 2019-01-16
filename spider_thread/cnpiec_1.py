
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
        urls.append("http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index.html")
        for i in range(3000):
            urls.append("http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_"+str(i+1)+".html")
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

        for li in soup.find_all("li"):
            url_n = "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg" + li.find("a")["href"][1:]
            date=li.find("span").text
            result = self.url_increment.is_increment(url_n, date)
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "gbk"
        data = resq.text
        date=self.get_date(data)
        title=self.get_title(data)
        text=self.get_text(data)
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

    def get_date(self,html):
        str3 = '<span class="datetime" style="float:right;margin-right: 52px">.*</span>'
        patten3 = re.compile(str3)
        result3 = patten3.findall(html)
        date = result3[0][62:-7]
        return date

    def get_title(self,html):
        str4 = '<span style="font-size: 20px;font-weight: bold">.*\n?.*</span>'
        patten4 = re.compile(str4)
        result4 = patten4.findall(html)
        soup = BeautifulSoup(result4[0], "html.parser")
        return soup.find_all("span")[0].get_text().strip().replace("\n", " ")

    def get_text(self,html):
        test_result = re.search('<div align="left" style="padding-left:30px;">', html)
        data_div_front = html[test_result.span()[1]:]
        test_result = re.search('</div>', data_div_front)
        data_div = data_div_front[0:test_result.span()[0]]

        str = ""

        soup = BeautifulSoup(data_div, "html.parser")
        [s.extract() for s in soup('style')]

        for tag in soup.find_all("p"):
            str = str + tag.get_text().strip()

        return str.replace("\n", "")









if __name__ == '__main__':
    j = job.Job("cnpiec_1")
    j.submit("first","second","thrid",pyname="cnpiec_1")

