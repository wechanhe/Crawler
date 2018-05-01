#-*- encoding:utf-8 -*-
import requests

from bs4 import BeautifulSoup

seed = "http://news.qq.com/"

# 获取各栏目URL
def getURLs(seed):
    seeds = []
    seeds.append(seed)
    textdata = requests.get(seed).text
    soup = BeautifulSoup(textdata,'lxml')
    nodes = soup.select("div.stitle > a.more")
    for n in nodes:
        link = n.get("href")
        seeds.append(link)
    # print(seeds)
    return seeds

# 请求腾讯新闻的URL
def getNewsURL(news_url):
    result = []
    for url in news_url:
        wbdata = requests.get(url).text

        # 对获取到的文本进行解析

        soup = BeautifulSoup(wbdata, 'lxml')

        # 从解析文件中通过select选择器定位指定的元素，返回一个列表

        major = soup.select("div.text > em.f14 > a.linkto")  # 要闻

        # 对返回的列表进行遍历
        for n in major:
            title = n.get_text()
            link = n.get("href")
            result.append(link)

    print(result)
    return result

# 获取html文本
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # r.encoding = 'utf-8'
        return r.text
    except:
        return ""

# 解释网页内容，过滤得到新闻标题和内容，并写入文件
def getContent(url,i):
    html = getHTMLText(url)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("div.LEFT > h1")
    if len(title) < 1:
        return False
    print(title[0].get_text())
    # time = soup.select("div.a_Info > span.a_time")
    # print(time[0].string)
    # author = soup.select("div.qq_articleFt > div.qq_toolWrap > div.qq_editor")
    # print(author[0].get_text())
    paras = soup.select("div.content-article > p.one-p")
    # for para in paras:
    #     if len(para) > 0:
    #         print(para.get_text())
    #         print()
    # 写入文件
    fo = open("data/"+str(i)+".txt", "w+",encoding='utf-8')
    fo.writelines(title[0].get_text() + "\n")
    for para in paras:
        if len(para) > 0:
            fo.writelines(para.get_text() + "\n\n")
    fo.close()
    return True

def main():
    i = 1
    urls = getNewsURL(getURLs(seed))
    for url in urls:
        if getContent(url,i):
            i += 1

main()