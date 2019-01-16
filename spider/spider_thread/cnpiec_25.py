
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
        urls_t = ["http://zbb.njau.edu.cn/pgoods", "http://zbb.njau.edu.cn/pservices",
                  "http://zbb.njau.edu.cn/pprojects", "http://zbb.njau.edu.cn/pquick"]

        for url in urls_t:
            html = self.get_html(url + "/index.jhtml")

            soup = BeautifulSoup(html, "html.parser")

            for tag in soup.find_all("div", class_="lpage"):
                tt = tag.get_text()
                n = re.search("/.*页", tag.get_text()).span()
                num = tt[n[0] + 1:n[1] - 1]
                for i in range(int(num)):
                    if i == 0:
                        urls.append(url + "/index.jhtml")
                    else:
                        urls.append(url + "/index_" + str(i + 1) + ".jhtml")
        return urls

    def get_html(self,url):
        data = requests.get(url)
        data.encoding = 'utf-8'
        data = data.text
        return data

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        try:
            data = requests.get(url)
            data.encoding = 'utf-8'
            data = data.text
        except:
            return self.attr.DONE
        soup = BeautifulSoup(data, "html.parser")
        dl_tag = soup.find("dl", class_="llist")
        for dd_tag in dl_tag.find_all("dd", cid="4"):
            url_n = dd_tag.find("a")["href"]
            date = dd_tag.find("span").text
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
        tag = soup.find("div", class_="lright cright")
        ctitle = tag.find("div", class_="ctitle")
        text = tag.find_all(attrs={'class': 'ccontent'})[0].get_text().strip()
        title = tag.find("h1").get_text()
        date = ctitle.find("i").get_text().strip()[6:]
        text = "".join(text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

if __name__ == '__main__':
    j = job.Job("cnpiec_25")
    j.submit("first","second","thrid",pyname="cnpiec_25")

