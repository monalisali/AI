#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Spider.py
@Time    :   2021/06/04 02:20:24
@Author  :   YuFanWenShu 
@Contact :   1365240381@qq.com
'''

# here put the import lib

import json
import requests
import time
import random

#import yaml

#with open("wechat.yaml", "r") as file:
#    file_data = file.read()
#config = yaml.safe_load(file_data) 

#header:appmsgpublish?sub=list&search_field=nullXXXXXX
headers = {
    "Cookie": "appmsglist_action_3198942316=card; yyb_muid=1C253B2D4F7A64CE0EFD2D6C4E5465DB; ua_id=xYjzpVujyIAdIM3ZAAAAAAZJyXHShJ_U3RLizy-VwvM=; wxuin=54548910062116; noticeLoginFlag=1; mm_lang=zh_CN; _clck=3198942316|1|fyl|0; cert=LJKot2wyTMiXiFuxkbWuz0Zgyd69ICPC; uuid=1d0cf6bc24ea57d70db01858ecca2aba; bizuin=3198942316; ticket=6c2011ed30f9285c9318db8d9a2a9f21e285e718; ticket_id=gh_5a6956c93013; slave_bizuin=3198942316; rand_info=CAESIEK1OOeET0xwrWWKjIakesL0F6ndjzVMFlmED4UATXWA; data_bizuin=3198942316; data_ticket=LrMfv1c7+HJUWM8R0AS0O6D3NZf8ZGwpSfNYkgfH/XUClPMHx2RArrOj6yUjaPoJ; slave_sid=bnBlV294c29ISjZQMGVsS0RYYlc0QWpoWGxfWjlfWFNYSWVnUERIa0VxNmZBZ3Z4WGlUVzk4dVBoUkp0NmJLekFhWEptTDdSdnBETGJVNk16bHZ0bnJwbG1WNkdhTDllN3VOMEhMNzJ2NU9zMWJ0a2p3VlNvYkhwcmJGSHNqelNQT1BoZU05VnFYa0pkVnFa; slave_user=gh_5a6956c93013; xid=2dfa0f1b72428e800712f79cbf673534; openid2ticket_obPyrvnacYnUf9lm5vm8rBfVwObo=MSMFnH2Ja87F1fNXcJ8RBZLLNVBmxc2n93srOH+iGUA=; _clsk=17loqdz|1755588542043|6|1|mp.weixin.qq.com/weheat-agent/payload/record",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

# 请求参数
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
begin = "0"
params = {
    "action": "list_ex",
    "begin": begin,
    "count": "5",
    "fakeid": "MjM5MDU2MTc4NQ%3D%3D", #爬取目标的公众号id。
    # 上海经信委: "MjM5MDU2MTc4NQ%3D%3D"
    # 北邮家教部: "MjM5NDY3ODI4OA%3D%3D", 测试用
    "type": "9",
    "token": 1423536479,
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1"
}

# 存放结果
app_msg_list = []
# 在不知道公众号有多少文章的情况下，使用while语句
# 也方便重新运行时设置页数
with open("app_msg_list.csv", "w",encoding='utf-8') as file:
    file.write("文章标识符aid,标题title,链接url,时间time\n")
i = 0
while True:
    if i == 10:
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
            info = '"{}","{}","{}","{}"'.format(str(item["aid"]), item['title'], item['link'], str(item['create_time']))
            with open("app_msg_list.csv", "a",encoding='utf-8') as f:
                f.write(info+'\n')
        print(f"第{i}页爬取成功\n")
        print("\n".join(info.split(",")))
        print("\n\n---------------------------------------------------------------------------------\n")

    # 翻页
    i += 1    