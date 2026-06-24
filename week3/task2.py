from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import csv
import re
# 流程
# 1. 獲得頭三頁的內容，透過讀取下一頁herf
# 2. 過濾第一頁的公告？
# 3. 逐篇進入獲取日期與毒外面的推數
articles_path = Path("articles.csv")


def next_page(path):
    url = "https://www.ptt.cc"+ path
    data_ptt = urllib.request.urlopen(url).read().decode('utf-8')
    site = BeautifulSoup(data_ptt,'html.parser')
    btns = site.select(".btn-group-paging a")
    for i in btns:
        if i.get_text() == "‹ 上頁":
            return i["href"]
               
def get_page(path):
    ptt_url = "https://www.ptt.cc"+ path
    data_ptt = urllib.request.urlopen(ptt_url).read().decode('utf-8')

    site = BeautifulSoup(data_ptt,'html.parser')

    titles = site.select('.r-ent .title')
    push_count = site.select('.r-ent .nrec')
    article_list = []
    for i,v in enumerate(titles):
        a_tag = v.find('a')
        if not a_tag:
            continue  
        else:
            sp_url = "https://www.ptt.cc"+ a_tag["href"]
            data_sp = urllib.request.urlopen(sp_url).read().decode('utf-8')
            sp = BeautifulSoup(data_sp,'html.parser')
            fir = sp.select(".article-metaline .article-meta-value")
            time = sp.select(".f4.b7")
            pa = r'^[a-zA-Z]{3}\s+[a-zA-Z]{3}\s+[0-9]{1,2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s+[0-9]{4}'
            if fir:
                for j in fir:
                    j_str = j.get_text()
                    if re.match(pa, j_str):
                        article_list.append([v.get_text(strip=True), push_count[i].get_text(strip=True),j_str])
            if time:
                for str in time:
                    if str.get_text() ==  " 時間 " :
                        sec = sp.select(".b4")
                        for j in sec:
                            j_str = j.get_text().strip()
                            if re.match(pa, j_str):
                                article_list.append([v.get_text(strip=True), push_count[i].get_text(strip=True) ,j_str])
            if not fir and not time:
                article_list.append([v.get_text(strip=True), push_count[i].get_text(strip=True),''])
    return article_list

ptt_url="/bbs/Steam/index.html"
needs = 3
ans = []
n_url = ptt_url
for i in range(needs):
    ans.extend(get_page(n_url))
    n_url = next_page(n_url)

with open(articles_path,"w",newline="",encoding="utf-8")as f:
    writer = csv.writer(f)
    writer.writerows(ans)