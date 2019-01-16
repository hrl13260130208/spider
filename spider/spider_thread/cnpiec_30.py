
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
        for num in range(1311):
            urls.append(
                "http://www.ccgp-qinghai.gov.cn/jilin/zbxxController.form?declarationType=&type=1&pageNo=" + str(num))
        return urls


class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        try:
            data = requests.get(url)
            data.encoding = 'utf-8'
            data = data.text
        except:
            self.attr.DONE
        soup = BeautifulSoup(data, "html.parser")

        div_tag = soup.find("div", class_="m_list_3")
        for li_tag in div_tag.find_all("li"):
            a_tag = li_tag.find("a")
            url_n = a_tag["href"]
            date = li_tag.find("span").text
            date = date.replace("年", "-")
            date = date.replace("月", "-")
            date = date.replace("日", "")
            result = self.url_increment.is_increment(url_n, date)
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):

        dnum = re.search("(\d{4}/\d{1,2}/\d{1,2})", url).span()
        date = url[dnum[0]:dnum[1]]

        suffix_num = re.search("htmlURL=", url).span()
        suffix = url[suffix_num[1]:]
        new_url = "http://www.ccgp-qinghai.gov.cn/" + suffix
        data = requests.get(new_url)
        data.encoding = 'GBK'
        data = data.text
        soup = BeautifulSoup(data, "html.parser")


        tag = soup.find("body")

        title = ""
        for p_title in tag.find_all("p", align="center"):
            title = title + p_title.get_text().strip()
            p_title.extract()

        [s.extract() for s in tag('input')]

        text = tag.get_text().strip()
        text = "".join(text.split())
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line



def test():
    url="http://www.ccgp-qinghai.gov.cn/jilin/zbxxController.form?declarationType=&type=1&pageNo=1"
    data = requests.get(url)
    data.encoding = 'utf-8'
    data = data.text

    soup = BeautifulSoup(data, "html.parser")

    div_tag = soup.find("div", class_="m_list_3")
    for li_tag in div_tag.find_all("li"):
        a_tag = li_tag.find("a")
        url_n = a_tag["href"]
        date = li_tag.find("span").text
        date=date.replace("年","-")
        date=date.replace("月","-")
        date=date.replace("日","")
        print(url_n, date)

if __name__ == '__main__':

    j = job.Job("cnpiec_30")
    j.submit("first","second","thrid",pyname="cnpiec_30")
    # j.clear_schedule()
