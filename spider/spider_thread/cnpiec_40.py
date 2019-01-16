
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
        for i in range(872):
            urls.append("http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002002/?Paging="+str(i+1))
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        data = requests.get(url)
        data.encoding = "gbk"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        td_tag = soup.find("td", height="800")
        table_tag = td_tag.find("table", width="98%")
        for tr in table_tag.find_all("tr"):
            a = tr.find("a")
            date = tr.find("td", width="90")
            if a == None:
                continue
            url_n = "http://ggzy.xjbt.gov.cn" + a["href"]
            result = self.url_increment.is_increment(url_n, date.text[1:-1])
            if result:
                urls.append(url_n)
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        resq = requests.get(url)
        resq.encoding = "gbk"
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
        start = data.find(
            '<table cellspacing="0" cellpadding="0" border="0" style="border-width:0px;width:748px;border-collapse:collapse;">')
        end = data.find('</table></body>')
        text = data[start:end]
        p = re.compile('(?<=\>).*?(?=\<)')
        result = p.findall(text)
        text = "".join(result).replace("&nbsp;", "")
        if text == "":
            div = table_tag.find("div", class_="infodetail")
            [s.extract() for s in div("style")]
            text = div.text
        text = "".join(text.split())
        if text == "":
            return self.attr.DONE
        line = url + "##" + date + "##" + title + "##" + text + "\n"
        return line

def test():
    urls = []
    url="http://ggzy.xjbt.gov.cn/TPFront/jyxx/004002/004002002/?Paging=6"
    data = requests.get(url)
    data.encoding = "gbk"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    td_tag=soup.find("td",height="800")
    table_tag=td_tag.find("table",width="98%")
    for tr in table_tag.find_all("tr"):
        a=tr.find("a")
        date=tr.find("td",width="90")
        if a ==None:
            continue
        url_n="http://ggzy.xjbt.gov.cn"+a["href"]
        print(url_n,date.text[1:-1])


    return urls

def test2():
    url="http://ggzy.xjbt.gov.cn/TPFront/infodetail/?infoid=4ebc9a79-1a74-457a-b262-f7186e64aa18&CategoryNum=004002002"

    resq=requests.get(url)
    resq.encoding = "gbk"
    data=resq.text
    soup=BeautifulSoup(data,"html.parser")
    table_tag = soup.find("table", id="tblInfo")
    td_tag = table_tag.find("td", id="tdTitle")
    t_font = td_tag.find("font", style="font-size: 25px")
    d_font = td_tag.find("font", class_="webfont")
    title = t_font.text.strip()
    d_line = d_font.text.strip()
    end = d_line.find("】")
    date = d_line[6:end].strip().replace("/", "-")
    start=data.find('<table cellspacing="0" cellpadding="0" border="0" style="border-width:0px;width:748px;border-collapse:collapse;">')
    end =data.find('</table></body>')
    text=data[start:end]
    p = re.compile('(?<=\>).*?(?=\<)')
    result = p.findall(text)
    text = "".join(result).replace("&nbsp;","")
    if text=="":
        div=table_tag.find("div",class_="infodetail")
        print(div)
        text=div.text
    text = "".join(text.split())
    print(text=="")
    line = url + "##" + date + "##" + title + "##" + text + "\n"
    print(line)
    return line






if __name__ == '__main__':
    j = job.Job("cnpiec_40")
    j.submit("first","second","thrid",pyname="cnpiec_40")

