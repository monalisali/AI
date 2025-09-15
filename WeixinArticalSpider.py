# here put the import lib
import json
import requests
import time
import random
import os
from datetime import datetime
from pathlib import Path

def startToReadArtical():
     artical_path = Path("ArticalData")
     if not artical_path.exists():
         artical_path.mkdir(parents=True,exist_ok=True)

     with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        articalList = fcc_data["articalList"]
        for o in articalList:
            readWeixinArtical(o,dir=artical_path)
            #print(o["officalAccout"])
           

def readWeixinArtical(itemConfig,dir):
    # 目标公众号的fakeId
    fakeId = itemConfig["fakeId"]
    with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        appData = json.load(fcc_file) 
    headers = {
        "Cookie": appData["cookieStr"],
        "User-Agent": appData["userAgent"]
    }

    # 请求参数
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    begin = "0"
    params = {
        "action": "list_ex",
        "begin": begin,
        "count": "5",
        "fakeid": fakeId, #爬取目标的公众号id。
        # 上海经信委: "MjM5MDU2MTc4NQ%3D%3D"
        # 北邮家教部: "MjM5NDY3ODI4OA%3D%3D", 测试用
        "type": "9",
        "token": appData["token"],
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }

    # 存放结果
    app_msg_list = []
    # 在不知道公众号有多少文章的情况下，使用while语句
    # 也方便重新运行时设置页数
    fileSuffix = datetime.now().strftime('%Y%m%d')
    fileName = dir / f"app_msg_list_{fileSuffix}.csv"
    if not os.path.exists(fileName):
        with open(fileName, "w",encoding='utf-8-sig') as file:
            file.write("文章标识符aid,标题title,链接url,时间time,公众号名称\n")

    i = 0
    while True:
        # 爬取到第几页就停止
        if i == 1:
            break
        
        begin = i * 5
        params["begin"] = str(begin)
        # 随机暂停几秒，避免过快的请求导致过快的被查到
        time.sleep(random.randint(1,10))
        resp = requests.get(url, headers=headers, params = params, verify=False,timeout=60)
        # 微信流量控制, 退出
        if resp.json()['base_resp']['ret'] == 200013:
            print("frequencey control, stop at {}".format(str(begin)))
            time.sleep(3600)
            continue
        
        # 如果返回的内容中为空则结束
        if len(resp.json()['app_msg_list']) == 0:
            print("all ariticle parsed")
            break
            
        msg = resp.json()
        if "app_msg_list" in msg:
            for item in msg["app_msg_list"]:
                timeStamp = item['create_time']
                publishTime = datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d')
                info = '"{}","{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'], str(publishTime)
                                                    ,itemConfig["officalAccout"])
                with open(fileName, "a",encoding='utf-8-sig') as f:
                    f.write(info+'\n')
            print(f"第{i}页爬取成功\n")
            print("\n".join(info.split(",")))
            print("\n\n---------------------------------------------------------------------------------\n")

        # 翻页
        i += 1    

startToReadArtical()