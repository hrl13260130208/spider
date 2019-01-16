
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
        url = "http://soeasycenter.com/newTender"

        parm = {
            "periodTime": " 0.0",
            "pageNum": "1",
            "pageSize": "500",
        }

        data = requests.post(url, data=parm)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find("table", class_="table table-striped")
        [s.extract() for s in table('thead')]
        for tr_tag in table.find_all("tr"):
            a_tag = tr_tag.find("a")
            url_n = "http://soeasycenter.com" + a_tag["href"]
            date = tr_tag.find_all("td")[3].text
            result = self.url_increment.is_increment(url_n, date)
            if result:
                urls.append(url_n)

        return urls


class second(ss.ThreadingSpider):

    def get(self,url):
       pass

class thrid(ss.ThreadingSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = 'UTF-8'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="maincontent")
        fdiv = div_tag.find("div", class_="mytop")
        title = fdiv.find("h4").get_text().strip()
        date = fdiv.find("p").get_text().strip()
        b_num = re.search("发布时间：", date).span()
        e_num = re.search("来源：", date).span()
        date = date[b_num[1]:e_num[0]].strip()
        text = div_tag.find("div", class_="mymain").get_text().strip()
        text = "".join(text.split())

        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line



def test():
    url = "http://soeasycenter.com/newTender"

    parm = {
        "periodTime": " 0.0",
        "pageNum": "1",
        "pageSize": "500",
    }

    data = requests.post(url, data=parm)
    data.encoding = "utf-8"
    data = data.text

    soup = BeautifulSoup(data, "html.parser")

    table = soup.find("table", class_="table table-striped")
    [s.extract() for s in table('thead')]
    for tr_tag in table.find_all("tr"):
        a_tag=tr_tag.find("a")
        url_n="http://soeasycenter.com" + a_tag["href"]
        date=tr_tag.find_all("td")[3].text
        print(url_n,date)



if __name__ == '__main__':
    j = job.Job("cnpiec_31")
    j.submit("first","thrid",pyname="cnpiec_31")

