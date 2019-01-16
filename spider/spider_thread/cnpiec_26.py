
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
        urls_t = ["http://www.njgp.gov.cn/cgxx/cggg/jzcgjg/", "http://www.njgp.gov.cn/cgxx/cggg/bmjzcgjg/",
                  "http://www.njgp.gov.cn/cgxx/cggg/qjcgjg/", "http://www.njgp.gov.cn/cgxx/cggg/shdljg/",
                  "http://www.njgp.gov.cn/cgxx/cggg/qtbx/"]

        for url in urls_t:
            html = self.get_html(url + "index.html")

            soup = BeautifulSoup(html, "html.parser")

            for tag in soup.find_all("div", class_="page_turn"):
                tt = tag.find_all("script")[1].get_text().strip()

                n = tt.split(",")[0]
                num = n[15:]
                for i in range(int(num)):
                    if i == 0:
                        urls.append(url + "index.html")
                    else:
                        urls.append(url + "index_" + str(i) + ".html")
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
        nums = re.search("index", url).span()
        prefix = url[:nums[0]]

        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="R_cont_detail")
        for li_tag in div_tag.find_all("li"):
            a_tag = li_tag.find("a")
            url_t = a_tag["href"]
            url_n = prefix + url_t[2:]
            [s.extract() for s in li_tag("a")]
            date = li_tag.text.strip()
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
        tag = soup.find("div", class_="cont")
        title = tag.find("div", class_="title").get_text().strip()
        date = tag.find("div", class_="extra")
        [s.extract() for s in date('span')]
        tdate = date.get_text().strip()
        num = re.search("作者", tdate).span()
        date = tdate[5:num[0]].strip()
        text = tag.find("div", class_="article")
        [s.extract() for s in text('script')]
        [s.extract() for s in text('style')]

        text = text.get_text().strip()
        text = "".join(text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line



def test():
    url="http://www.njgp.gov.cn/cgxx/cggg/jzcgjg/index.html"
    data = requests.get(url)
    data.encoding = 'utf-8'
    data = data.text
    nums = re.search("index", url).span()
    prefix = url[:nums[0]]

    soup = BeautifulSoup(data, "html.parser")

    div_tag = soup.find("div", class_="R_cont_detail")
    for li_tag in div_tag.find_all("li"):
        a_tag = li_tag.find("a")
        url_t = a_tag["href"]
        url_n = prefix + url_t[2:]
        [s.extract() for s in li_tag("a")]
        date=li_tag.text.strip()
        print(url_n, date)

if __name__ == '__main__':
    j = job.Job("cnpiec_26")
    j.submit("first","second","thrid",pyname="cnpiec_26")

