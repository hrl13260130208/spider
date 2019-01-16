
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
        list = ['shengji/', 'nanjing/', 'suzhou/', 'wuxi/', 'changzhou/', 'zhenjiang/', 'nantong/', 'taizhou/',
                'yangzhou/', 'yancheng/', 'huaian/', 'suqian/', 'lianyungang/', 'xuzhou/']
        for i in list:
            i_url = "http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/" + i

            self.get_next_page_url(i_url, urls)
        return urls

    def get_next_page_url(self,url, urls):
        html = self.get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        div_tag = soup.find_all("div", class_="fanye")[0]
        script = div_tag.find_all("script", language="JavaScript")
        string = script[0].get_text().strip()
        num = re.search(',', string).span()[0]
        max_page = string[15:num]
        for i in range(int(max_page)):
            if i == 0:
                urls.append(url + "index.html")
                continue
            urls.append(url + "index_" + str(i) + ".html")

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
        num = re.search("/index", url).span()[0]
        url = url[:num]
        div = soup.find("div", class_="list_list")
        if div is None:
            div = soup.find("div", class_="list_list02")
        for li_tag in div.find_all("li"):

            a_tag = li_tag.find("a")["href"]
            url_n = url + a_tag[1:]

            date = li_tag.find("span").text
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
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        title = soup.find("h1").get_text().strip().replace("\n", "")
        date_div = soup.find("div", class_="detail_bz")
        date = date_div.find("span").get_text().strip().replace("\n", "")[6:]
        text = soup.find("div", class_="detail_con").get_text().strip().replace("\n", "")
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

if __name__ == '__main__':
    j = job.Job("cnpiec_21")
    j.submit("first","second","thrid",pyname="cnpiec_21")
    # j.clear_schedule()
