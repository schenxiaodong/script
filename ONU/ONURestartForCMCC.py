import requests
import re

# 首先获取 GetRandCount
GetRandCountUrl = "http://192.168.1.1/asp/GetRandCount.asp"
GetRandCountResponse = requests.request("POST", GetRandCountUrl, headers={}, data={})
# 设置Response 的编码格式
GetRandCountResponse.encoding = "UTF-8"
RandCount = GetRandCountResponse.text
# 字符串只保留英文和数字，获取的就是RandCountToken
RandCount = re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", "", RandCount)

# 然后进行登录获取cookie
getCookieUrl = "http://192.168.1.1/login.cgi"
# 拼接参数，x.X_HW_Token为上面的token
getCookiePayload = 'UserName=用户名&PassWord=BASE64加密后的密码&x.X_HW_Token=' + RandCount
getCookieHeaders = {
    'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
    'Accept': '*/*',
    'Host': '192.168.1.1',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", getCookieUrl, headers=getCookieHeaders, data=getCookiePayload)
# 获取cookie字符串，但是cookie中参数过多，所有进行删除一部分内容
cookieStr = response.headers.get("Set-cookie")
cookie = cookieStr[0:cookieStr.rfind(";")]

# 获取重启按钮的Token
getRestartButtonUrl = "http://192.168.1.1/html/ssmp/devmanage/cmccdevicereset.asp"
getRestartButtonHeaders = {
    'Cookie': cookie,
    'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
    'Accept': '*/*',
    'Host': '192.168.1.1',
    'Connection': 'keep-alive'
}
getRestartButtonResponse = requests.request("GET", getRestartButtonUrl, headers=getRestartButtonHeaders, data={})
getRestartButtonResponse.encoding = "UTF-8"
htmlDom = getRestartButtonResponse.text
# 需要对返回的html进行解析获取到token
obj = re.compile('hwonttoken.*')
result = obj.search(htmlDom);
resultStr = result[0]
getRestartButtonToken = resultStr[(resultStr.find("=\"") + 2): resultStr.rfind("\"")]

# 重启路由器
RestartUrl = "http://192.168.1.1/html/ssmp/devmanage/set.cgi?x=InternetGatewayDevice.X_HW_DEBUG.SMP.DM.ResetBoard&RequestFile=html/ssmp/devmanage/cmccdevicereset.asp"
RestartPayload = 'x.X_HW_Token=' + getRestartButtonToken
RestartHeaders = {
    'Cookie': cookie,
    'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
    'Accept': '*/*',
    'Host': '192.168.1.1',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded'
}
# 使用try catch将报错的信息隐藏（重启的时候避免内存消耗故意将超时时间设为10s）
try:
    RestartResponse = requests.request("GET", RestartUrl, headers=RestartHeaders, data=RestartPayload, timeout=10)
except Exception as e:
    i = 1
