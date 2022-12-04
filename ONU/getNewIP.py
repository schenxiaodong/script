import requests
import re
## 中国电信光猫通过接口进行重启
#登录，获取短暂性token,暂不清楚机制，貌似是登录一下之后该主机不需要再次获取token
url = "http://192.168.1.1/login.cgi"

payload='username=账号&password=密码&save=%25B5%25C7%25C2%25BC'
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
   'Accept': '*/*',
   'Host': '192.168.1.1',
   'Connection': 'keep-alive',
   'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

#print(response.text)

# 获取session id，用于重启
url1 = "http://192.168.1.1/MD_Device.html"

payload1={}
headers1 = {
   'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
   'Accept': '*/*',
   'Host': '192.168.1.1',
   'Connection': 'keep-alive'
}

response1 = requests.request("GET", url1, headers=headers1, data=payload1)

# print(response.text)
resultText = response1.text;
obj = re.compile('sessionKey.*')
result = obj.search(resultText);
sessionKey = result[0].split("'")[1]
#print(sessionKey)

url2 = "http://192.168.1.1/rebootinfo.cgi?sessionKey=" + sessionKey

payload2={}
headers2 = {
   'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
   'Accept': '*/*',
   'Host': '192.168.1.1',
   'Connection': 'keep-alive'
}
### 执行重启
response2 = requests.request("GET", url2, headers=headers2, data=payload2)
response2.encoding = "GB2312"  # 设置字符集
print(response2.text)
