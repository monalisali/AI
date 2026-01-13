# here put the import lib
import json
import requests
import time
import random
import os
from datetime import datetime
from pathlib import Path
import log_config as log
import re
from collections import defaultdict

class Artical:
    def __init__(self,id,title,url,time,name,content):
        self.文章标识符aid = id.strip('"')
        self.标题title = title.strip('"')
        self.链接url = url.strip('"')
        self.时间time = time.strip('"')
        self.公众号名称 = name.strip('"')
        self.finalContent = content.strip('"')
    
    def to_dict(self):
        return {
            "文章标识符aid": self.文章标识符aid,
            "标题title": self.标题title,
            "链接url": self.链接url,
            "时间time":self.时间time,
            "公众号名称":self.公众号名称,
            "finalContent":self.finalContent
        }

def startToReadArtical():
     artical_path = Path("ArticalData")
     if not artical_path.exists():
         artical_path.mkdir(parents=True,exist_ok=True)
     
     # 读取app.json中的articalList参数是待读取的公众号的配置信息
     with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        fcc_data = json.load(fcc_file)
        articalList = fcc_data["articalList"]
        fileSuffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        fileName = artical_path / f"app_msg_list_{fileSuffix}.csv"
        for o in articalList:
            readWeixinArtical(o,fileName)
        
        log.logging.info("生成url文件： " + str(fileName.resolve()))    
        return str(fileName.resolve())

           
# 读取指定公众号的文章
# 参数: 
# itemConfig: 公众号的配置信息
# dir: 存放文件的目录
def readWeixinArtical(itemConfig,fileName):
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
    if not os.path.exists(fileName):
        with open(fileName, "w",encoding='utf-8-sig') as file:
            file.write("文章标识符aid,标题title,链接url,时间time,公众号名称\n")
    
    # 在不知道公众号有多少文章的情况下，使用while语句
    # 也方便重新运行时设置页数
    print("\n\n---------------------------！！爬取URL开始！！-------------------------------------------------\n")
    i = 0
    while True:
        # !!!爬取到第几页就停止
        if i == appData["maxPagesToGet"]:
            break
        
        begin = i * 5
        params["begin"] = str(begin)
        # 随机暂停几秒，避免过快的请求导致过快的被查到
        time.sleep(random.randint(1,10))
        resp = requests.get(url, headers=headers, params = params, verify=False,timeout=60)
        if resp.json()['base_resp']['err_msg'] == 'invalid session':
            log.logging.info("app.json 中的'cookieStr' 和 token 可能过期了，请更新")
            print("app.json 中的'cookieStr 和 token'可能过期了，请更新")
            break

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
            print(f"第{i+1}页爬取成功\n")
            print("\n".join(info.split(",")))

        # 翻页
        i += 1
    
    print("\n\n---------------------------！！爬取URL结束！！-------------------------------------------------\n")    
    
    

def GetArticalConetent(fileFullName):
    print("\n\n------------------------！！生成公众号内容文件开始！！----------------------------------------------\n")
    log.logging.info("------------------------！！生成公众号内容文件开始！！----------------------------------------------")
    log.logging.info("读取url文件：" + str(fileFullName))
    print("读取url文件：", str(fileFullName))
    contentList= [] # 读取的文件内容
    taxPolicyArtical = []  # 税务相关的内容
    filePathList = [] #生成文件的路径
    with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        appData = json.load(fcc_file) 
    headers = {
        "Cookie": appData["cookieStr"],
        "User-Agent": appData["userAgent"]
    }

    with open(fileFullName, "r",encoding='utf-8-sig') as file:
        data = file.readlines()
        # print(data)
        n = len(data)
    for i in range(n):
        mes = data[i].strip("\n").split(",")
        if len(mes) != 5: #校验列头是否为5列
            continue
        url = mes[2].strip('"')
        text = ''
        if i > 0:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                text = cleanRespText(resp.text)
                contentList.append( Artical(mes[0], mes[1],url, mes[3],mes[4],text))
                log.logging.info("url内容读取完成：" + str(url))
                print("url内容读取完成：", str(url))

    fileSuffix = datetime.now().strftime('%Y%m%d')
    content_path = Path("ArticalData/contentFiles/" + fileSuffix)
    if not content_path.exists():
        content_path.mkdir(parents=True,exist_ok=True)
    #获取税务相关的文章
    for c in contentList:
        if getTaxPolicyArticalOnly(c) is not None:
            taxPolicyArtical.append(c)
    

    grpNames = defaultdict(list)
    for c in taxPolicyArtical:
        grpNames[c.公众号名称].append(c)
    # 公众号名称一样的内容放在一个文件中
    for n in grpNames:
        fileName = content_path / f"{n}_{fileSuffix}.md"
        with open(fileName, "w",encoding='utf-8-sig') as contentFile:
            convertedList = [art.to_dict() for art in taxPolicyArtical if art.公众号名称 == n]
            contentFile.write(json.dumps(convertedList,ensure_ascii=False)) #输出的内容要格式漂亮的话，可以带上indent=4参数
            filePathList.append(str(fileName.resolve()))
            log.logging.info("生成公众号内容文件：" + str(fileName.resolve()))
            print("生成公众号内容文件：", str(fileName.resolve()))
    
    log.logging.info("------------------------！！生成公众号内容文件结束！！----------------------------------------------")
    print("\n\n------------------------！！生成公众号内容文件结束！！----------------------------------------------\n")
    return filePathList
         

def cleanRespText(text):
    pattern = re.compile(
                r'<(?!/p\b)[^>]+>|'  # 匹配所有HTML标签，只保留</p>
                r'\s+(data|style|class|id|href|src|type|on\w+)="[^"]*"|'  # 匹配HTML属性
                r'\s+(data|style|class|id|href|src|type|on\w+)=\'[^\']*\''  # 匹配单引号的HTML属性
            )
    
    #截取正文数据
    text = text[text.rfind("rich_media_content js_underline_content"):text.rfind('<script type="text/javascript"')]
    #截取后的正文包含很多html和css代码，去掉它们
    text = pattern.sub('',text) 
    #尾部还有js代码，去掉它们
    text = text[text.find('">')+2:text.find('var')]
    #去除无用的空白和换行
    text = re.sub(r'\s+', ' ', text).strip()
    #文章中有些地方用了</p>没用换行符，所以要把</p>要替换成换行符
    text = text.replace("</p>",'\r')
    return text

# 获取税务相关的文章
# 参数: 
# articalObj: 文章对象
# 返回: 
# 如果enableTaxPolicyFilter为True并且文章标题中包含"税"字，则是“税务”相关内容，返回文章对象
# 如果app.json中enableTaxPolicyFilter为False，说明不用过滤“税务”内容，直接文章对象
def getTaxPolicyArticalOnly(articalObj):
    with open('./app.json', 'r',encoding='utf-8') as fcc_file:
        appData = json.load(fcc_file) 
    if appData["enableTaxPolicyFilter"] and articalObj.标题title.find("税") != -1:
        return articalObj
    elif not appData["enableTaxPolicyFilter"]:
        return articalObj
    else:
        return None




#ss = GetArticalConetent(r"C:\D\AI\ArticalData\app_msg_list_20251223_120845.csv")
#vv = "a"
#urlFileName = startToReadArtical()
#GetArticalConetent(urlFileName)