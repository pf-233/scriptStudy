# 导入 requests 包
import requests
import json
import Be
from urllib.parse import urlencode

# 返回 http 的状态码
print("requests")

# 发送请求
# data = {'type':'tag','tag_id':'632762c02eaf6e578875f7b4','p':1}
# post_data = urlencode(data)
headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "charset=utf-8",
"accept-language": "zh-CN,zh;q=0.9",
"content-type": "application/json",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
x = requests.get('https://mikanani.me/Home/Bangumi/2817', headers=headers)

# 返回 http 的状态码
print(x.status_code)

# 响应状态的描述
print(x.reason)

# 返回编码
print(x.apparent_encoding)
print(x.text)
