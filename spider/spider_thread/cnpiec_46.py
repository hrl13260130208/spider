
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.job as job
import time
import random
import json



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        for i in range(666):
            url = "http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?pageSize=15&pageNo=" + str(
                i) + "&sourceAnnouncementType=3001&url=http%3A%2F%2Fnotice.zcy.gov.cn%2Fnew%2FnoticeSearch"
            time.sleep(random.random() * 3)
            data = requests.get(url)
            data.encoding = "UTF-8"
            data = data.text
            josns = json.loads(data)
            items = josns["articles"]
            for item in items:
                id = item["id"]
                url_0 = "http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?noticeId=" + id + "&url=http%3A%2F%2Fnotice.zcy.gov.cn%2Fnew%2FnoticeDetail"
                urls.append(url_0)

        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
      pass


class thrid(ss.ThreadingSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "UTF-8"
        data = resq.text
        jsons = json.loads(data)
        title = jsons["noticeTitle"].replace("\n","")
        n_date = jsons["noticePubDate"]
        date = n_date.split(" ")[0]
        content = jsons["noticeContent"]
        soup = BeautifulSoup(content, "html.parser")
        [s.extract() for s in soup("style")]
        text = soup.text
        text = "".join(text.split())
        result = self.url_increment.is_increment(url, date)
        if result:
            line = url + "##" + date + "##" + title + "##" + text+"\n"
            return line
        else:
            return self.attr.DONE

if __name__ == '__main__':

    j = job.Job("cnpiec_46")
    j.submit("first","thrid",pyname="cnpiec_46")

