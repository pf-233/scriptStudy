# 导入 requests 包
import requests
import json
import os
import sys
import shutil
from urllib.parse import urlencode
from win32com.client import Dispatch

MAX_VALUE_INT = sys.maxsize
# 导入迅雷
thunderApp = Dispatch('ThunderAgent.Agent64.1')
thunderAppPath = "D:/迅雷下载/tmptorrent/"
thunderSavePath = "D:/迅雷下载/"

def readConfig(filePath : str):
    with open(filePath, encoding="utf-8") as json_file:
        config = json.load(json_file)
        return config

def saveConfigFile(configJson : dict, path : str) :
    with open(path, "w", encoding="utf-8") as json_file:
        # indent为多行缩进空格数，sort_keys为是否按键排序,ensure_ascii=False为不确保ascii，及不将中文等特殊字符转为\uXXX等
        json.dump(configJson, json_file,indent=2,sort_keys=True, ensure_ascii=False)    

# print(readConfig())
config = readConfig("config.json")
saveConfigFile(config, "configBackup.json")

print("orign config:" + json.dumps(config, indent=2, ensure_ascii=False))
# {"saveFile": saveFile, "moveFile": moveFile}
def movePath(savePath : list) :
    for file in savePath:
        if (not os.path.exists(file["moveFile"])) : {
            os.makedirs(file["moveFile"])
        }
        shutil.move(file["saveFile"], file["moveFile"])
        print(file)

def cleanFile(path : str) :
    shutil.rmtree(path)
    os.mkdir(path)
    

# post_data = urlencode(data)
headers = {
"Accept": "*/*",
"Accept-Encoding": "charset=utf-8",
"content-type": "application/json",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# 请求体的字段
dataSeq = {'type', 'tag_id', 'p'}
languageConditions = ('简', "CHS", "CHT")
# 分辨率
quality = ("1080")
teamDict = {
    "5d8b24be306f1a0007bd7998" : {"name": "Lilith-Raws", "order":0},
    "5d2214af306f1a0007b55b1b" : {"name": "星空字幕組", "order":5},
    "58a9c1c9f5dc363606ab42ec" : {"name": "喵萌奶茶屋", "order":10},
    "585439a6a8e01b4f37915fe0" : {"name":  "SweetSub", "order":15},
    "57a034aa5cc0696f1ce1a1b1" : {"name":  "桜都字幕组", "order":20},
    "person" : {"name":  "猎户不鸽压制", "order":30},
    "54bb896d76870aad3bb603cf": {"name":  "千夏字幕组", "order":40},
    "62ef95af22a4a100078d1431": {"name": "Billion Meta Lab", "order":50},
    "559d1f1db85ffe4359622f5e" : {"name":  "诸神字幕组", "order":60},
    "5539e73add3d5c0b4e82f1fb" : {"name":  "愛戀字幕社&漫貓字幕社", "order":70},
    "5753dd362165b9ba0c485cd2" : {"name": "悠哈璃羽字幕社", "order":80},
    "55c0575824180bc3647feb1c" : {"name":  "动漫国字幕组", "order":90},
    "6352bdbf6b7b65000731860b" : {"name":  "北宇治字幕组","order":100},
    "62db95890274d400071ac5a8" : {"name":  "爪爪字幕组", "order":110},
    "581b44bfee98e9ca20730e9a" : {"name":  "SweetSub&LoliHouse", "order":120},
    "61be15742525b00007a3cfb1" : {"name":  "MingY", "order":130}    
}

# 根据上面的进行排序，可以设置先用那个字幕组
def teamSort(item) :
    teamId = item["team"]
    return teamDict[teamId]["order"] if teamId in teamDict  else MAX_VALUE_INT


# 获取集数
def getPart(title : str, group : str):
    if group == '5d8b24be306f1a0007bd7998':
        # "[Lilith-Raws] 給不滅的你 / Fumetsu no Anata e S02 - 05 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4]"
        part = title[title.index(']') + 1 : title.index('[', 2)].strip().split(" ")[-1]
    elif group == "581b44bfee98e9ca20730e9a" :
        # "[SweetSub&LoliHouse] 手工少女!! / Do It Yourself!! - 07v2 [WebRip 1080p HEVC-10bit AAC][简繁日内封字幕]（检索用：DIY）"
        part = title[title.index(']') + 1 : title.index('[', 2)].strip().split(" ")[-1][0 : 2]
    elif group in ("54bb896d76870aad3bb603cf"):
        # "[千夏字幕组][孤独摇滚!_BOCCHI THE ROCK!][第05话][1080p_AVC][简体]"
        part = title.split('[')[3].strip(']')[1 : 3]
    elif group in ("55c0575824180bc3647feb1c", "6352bdbf6b7b65000731860b", "61be15742525b00007a3cfb1", "58a9c1c9f5dc363606ab42ec", "person" , "57a034aa5cc0696f1ce1a1b1", "62db95890274d400071ac5a8"): 
        # "[MingY] DIY部！！ / Do It Yourself!! [06][1080p][简日内嵌]（招募）",
        # "【喵萌奶茶屋】★10月新番★[Do It Yourself!!/DIY][05][1080p][简日双语][招募翻译]"
        # "[猎户不鸽压制] 宇崎学妹想要玩！ω Uzaki-chan wa Asobitai! S2 [08] [1080p] [简中内嵌] [2022年10月番]"
        # "[桜都字幕组] 宇崎酱想要玩耍！ω / Uzaki-chan wa Asobitai! Double [06][1080p][简繁内封]"
        # "【爪爪字幕组】★10月新番[孤独摇滚！/Bocchi the Rock!][07][1080p][AVC][简日双语][MP4][招募时轴特效]"
        # "[北宇治字幕组]Bocchi the Rock!/孤独摇滚！[07][1080P][HEVC_AAC][CHS][MKV]（字幕组招人内详）"
        #  "【动漫国字幕组】★10月新番[秋叶原冥途战争][07][1080P][简体][MP4]"
        part = title.split('[')[2].strip().strip(']')
    elif group in ("5d2214af306f1a0007b55b1b", "62ef95af22a4a100078d1431","5753dd362165b9ba0c485cd2"):
        # "[Billion Meta Lab][Do It Yourself!!][07][1080P][HEVC 10bit][CHS&CHT]"
        # "【悠哈璃羽字幕社】[UHA-WINGS][孤獨搖滾_Bocchi the Rock!][07][x264 1080p][CHT]"
        # "[星空字幕組][鏈鋸人 / Chainsaw Man][07][繁日雙語][1080P][WEBrip][MP4]（急招翻譯、校對）"
        part = title.split('[')[3].strip().strip(']')
    elif group in ('559d1f1db85ffe4359622f5e',"585439a6a8e01b4f37915fe0"):
        # "[诸神字幕组][致不灭的你 第二季][To Your Eternity S2][04][简日双语字幕][720P][CHS HEVC MP4]"
        # "[SweetSub][手工少女!!][Do It Yourself!!][07][WebRip][1080P][AVC 8bit][繁日雙語]（檢索用：DIY）"
        part = title.split('[')[4].strip().strip(']')
    elif group in ('5539e73add3d5c0b4e82f1fb',):
        # "[愛戀字幕社&漫貓字幕社][10月新番][手工少女!!][Do It Yourself!!][04][1080P][MP4][BIG5][繁中]"
        part = title.split('[')[5].strip().strip(']')
    else :
        print("gourp not supprot:" + group)
        part = 0
    return int(part)



# title = "[星空字幕組][鏈鋸人 / Chainsaw Man][07][繁日雙語][1080P][WEBrip][MP4]（急招翻譯、校對）"
# t1 = title.split('[')[3].strip().strip(']')
# print(t1)
# 获取title 和 magnet 数据
def getTitleAndMagnetList(resContent : str):
    jsonarr = resContent['torrents']
    minPart = 10000
    titleAndmagnet = []
    for torrent in jsonarr:
        title = torrent['title']
        if quality in title and any(lang in title for lang in languageConditions) and "外挂" not in title:
            team = torrent['team_id']
            if team == None and title.find("猎户不鸽压制") < 0:
                continue
            elif team == None and title.find("猎户不鸽压制") >= 0:
                team = "person"

            try :
                part = getPart(torrent['title'], team)
                minPart = min(minPart, part)
                titleAndmagnet.append({'title': torrent['title'], 'magnet' : torrent['magnet'], "team" : team, "content": torrent['content'][0][0], "part" : part})
            except :
                print("getPart error torrent:" + torrent['title'])
    return {"titleAndmagnet":titleAndmagnet, "minPart":minPart}
docker run -d \
  --name=qbittorrent \
  -e PUID=0 \
  -e PGID=0 \
  -e TZ=Etc/UTC \
  -e WEBUI_PORT=8080 \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -v /path/to/appdata/config:/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  linuxserver/qbittorrent:latest

docker run -d \
--name=plex1 \
  -e PUID=0 \
  -e PGID=0 \
  -e TZ=Etc/UTC \
  -p 32400:32400 \
  -v /path/to/library:/config \
  -v /path/to/tvseries:/tv \
  -v /path/to/movies:/movies \
  --restart unless-stopped \
  lscr.io/linuxserver/plex:latest

plex:
  image: linuxserver/plex
  container_name: plex
  ports:
    - 32400:32400
    - 1900:1900/udp
    - 3005:3005
    - 5353:5353/udp
  environment:
    - TZ=Asia/Shanghai
    - PUID=0
    - PGID=0
    - VERSION=docker
  volumes:
    - ./plex:/config
    - ./Downloads:/media/Bangumi
  restart: unless-stopped

# 解析title 和magnet 数据得到要下载的magnet
def getMagnetUrl(data : dict, nowPart : int):
    page_count = data["p"]
    titleAndmagnet = []
    minPart = nowPart + 2
    needQuery = nowPart + 1 != minPart 
    res = {"status_code":200}
    while (needQuery and data["p"] <= page_count) : 
        try :
            res = requests.post('https://bangumi.moe/api/torrent/search',json=data, headers=headers)
        except : 
            res.status_code = 202
        if (res.status_code != 200):
            print("error get data:" + json.dumps(data))
            return titleAndmagnet
        responseJson = json.loads(res.text)
        if (len(responseJson) == 0):
            return titleAndmagnet
        if data["p"] == 1 :
            page_count = responseJson["page_count"]
        data["p"] = data["p"] + 1
        thisResult = getTitleAndMagnetList(responseJson)
        minPart = min(minPart, thisResult["minPart"])
        titleAndmagnet.extend(thisResult["titleAndmagnet"])
        needQuery = nowPart + 1 != minPart
    return titleAndmagnet


# 获取比已经存在的数据大的集数
def getDownloadPartMagnet(titleAndmagnet : list, nowPart : int) :
    titleAndmagnet.sort(key=teamSort)
    download = []
    needPart = list(range(nowPart + 1, nowPart + 50))
    for magnet in titleAndmagnet :
        part = magnet["part"]
        if part in needPart :
            download.append(magnet)
            del needPart[needPart.index(part)] 
    return download
    

savePath = []
# 发送请求, 第一个数组是时间分的
for timeInd in range(len(config['time'])):
    # 获取每个时间里的资源列表
    resources = config['resources'][timeInd]
    # 遍历每个季度资源的列表
    for resInd in range(len(resources)):
        # 构造请求体，只有字段在dataSeq 的才放入
        data = {}
        for signal in resources[resInd]:
            if (signal in dataSeq) :
                data[signal] = resources[resInd][signal]
        
        nowPart = resources[resInd]["nowPart"]
        # 获取磁力链接
        titleAndmagnet = getMagnetUrl(data, nowPart)
        # 获取比当前集数大的所有集数去下载
        downloads = getDownloadPartMagnet(titleAndmagnet, nowPart)
        print("change download:" + json.dumps(downloads, indent=2, ensure_ascii=False))
        maxPart = nowPart
        for download in downloads :
            maxPart = max(maxPart, download["part"])
            manget = download["magnet"]
            fileName = download["content"]
            saveFile = thunderAppPath + fileName
            moveFile = thunderSavePath + config['time'][timeInd] + "/" + resources[resInd]["name"] + "/"
            savePath.append({"saveFile": saveFile, "moveFile": moveFile})
            print("savePath:" + json.dumps(savePath, ensure_ascii=False))
            thunderApp.AddTask(manget, fileName)
            thunderApp.CommitTasks()
        resources[resInd]["nowPart"] = maxPart

saveOption = input("""need to save config please input T else F
""")
if (saveOption == "T") :
    saveConfigFile(config, "config.json")
    print("save config complete")
else :
    print("skip save config ")

print("savePath:" + json.dumps(savePath, ensure_ascii=False))
saveConfigFile({"savePath" : savePath}, "savePath.json")
step = input("""wait download complete to move path...
        complete input 1
        exit input 2
""")
if (step == "1") :
    movePath(savePath)
    cleanFile(thunderAppPath)
else:
    exit






# # 返回 http 的状态码
# print(res.status_code)

# # 响应状态的描述
# print(res.reason)

# # 返回编码
# # print(x.apparent_encoding)

# # print(x.content)

# # print(x.headers)
# # print(x.text)
# jsondir = json.loads(res.text)
# #print(json.dumps(jsondir))

# jsonarr = jsondir['torrents']
# for torrent in jsonarr:
#     title = torrent['title']
#     languageConditions = ('简', "CHS", "CHT")
#     quality = ("1080")
#     if quality in title and any(lang in title for lang in languageConditions) :
#         print(torrent['title'])
#         print(torrent['magnet'])







