import json
import os
from datetime import datetime
from pathlib import Path

#print('hello, world')
#print('hello, world')

def testFunction():
    with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        #print(fcc_data)
        # #print(fcc_data["articalList"])
        officalList = fcc_data["articalList"]
        cookie = fcc_data["cookieStr"]
        token = fcc_data["token"]
        print(officalList)
        print("cookie： " + cookie)
        print("token: " + str(token))
        #for o in officalList:
            #print(o["officalAccout"])

def startToReadArtical():
     with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        #print(fcc_data)
        # #print(fcc_data["articalList"])
        officalList = fcc_data["articalList"]
        #print(officalList)
        for o in officalList:
            readWeixinArtical(o)
            print("公众号名称：" + o["officalAccout"])
            print("公众号fakeID：" + o["fakeId"])
            print(o["officalAccout"])

def readWeixinArtical(itemConfig):
    with open("test_list.csv", "w",encoding='utf-8') as file:
        file.write("文章标识符aid,标题title,链接url,时间time,公众号名称\n")
    
    info = '"{}","{}","{}","{}","{}"'.format("a", "b", "c", "d",itemConfig["officalAccout"])
    with open("test_list.csv", "a",encoding='utf-8') as f:
        f.write(info+'\n')
    

artical_path = Path("ArticalData")
if not artical_path.exists():
    artical_path.mkdir(parents=True,exist_ok=True)

date = datetime.fromtimestamp(1755656812).strftime('%Y%m%d')
fileName = artical_path / f"AA_{date}.csv"
with open(fileName, "w", encoding="utf-8-sig") as file:
    file.write("中文中文11\n") 

if os.path.exists(fileName):
    with open(fileName, "a", encoding="utf-8-sig") as file:
        file.write("哈哈哈哈22\n")   

# testFunction()
#startToReadArtical()