from pathlib import Path
import urllib.request
import json
import csv
from collections import Counter
import re

# csv讀取
hotels_path = Path("hotels.csv")
districts_path = Path("districts.csv")
hotels_cn_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
hotels_en_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

#  讀取資訊
data_cn = urllib.request.urlopen(hotels_cn_url, data=None, context=None).read().decode('utf-8')
data_en = urllib.request.urlopen(hotels_en_url, data=None, context=None).read().decode('utf-8')
j_h_cn : list = json.loads(data_cn)["list"]
j_h_en : list= json.loads(data_en)["list"]
total_hotels_list = []
districts_list=[]
cn_map = {item["_id"]: item for item in j_h_cn}
for x in j_h_en:
    cn_x = cn_map[x["_id"]]
    if cn_x :
        total_hotels_list.append((cn_x["旅宿名稱"].strip(),x["hotel name"].strip(),cn_x["地址"],x["address"],cn_x["電話或手機號碼"],cn_x["房間數"],))
        match = re.search(r'(\w+市)(\w+區)', cn_x["地址"])
        add = match.group(2) if match else "未知"
        districts_list.append((add,cn_x["房間數"]))
# print(len(total_hotels_list))
counts = Counter(map(lambda i:i[0],districts_list))
districts_names = [i[0] for i in districts_list]
# 1.地區列表。2.以地區lost做雙重for迴圈
districts_set = set(districts_names)
districts = []
for i in districts_set:
    counter = 0
    for j in districts_list:
        if j[0] == i :
            counter += int(j[1])
    districts.append((i,str(counts[i]),str(counter)))
print(len(districts_set))
with open(hotels_path,"w",newline="",encoding="utf-8")as f:
    writer = csv.writer(f)
    writer.writerows(total_hotels_list)

with open(districts_path,"w",newline="",encoding="utf-8")as f:
    writer = csv.writer(f)
    writer.writerows(districts)