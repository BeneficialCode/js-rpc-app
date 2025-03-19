import requests
import hashlib

account = "17381560710"
password = '12345'
password = hashlib.md5(password.encode()).hexdigest()
url = f"https://passport.zcool.com.cn/login_jsonp_active.do?jsonpCallback=jQuery19107401774217245223_1742350591968&appId=1006&username={account}&password={password}&autoLogin=1&code=&service=https%3A%2F%2Fwww.zcool.com.cn%2F&appLogin=https%3A%2F%2Fwww.zcool.com.cn%2Flogin_cb&random=174235059197012663150&_=1742350591970"

payload = {}
headers = {
  'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'Connection': 'keep-alive',
  'Referer': 'https://passport.zcool.com.cn/login.do?appId=1006&appLogin=https://www.zcool.com.cn/login_cb&cback=https://www.zcool.com.cn/&thirdLogin=&regCback=&regFrom=',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Cookie': 'HWWAFSESID=d8e6e73eebc761941e; HWWAFSESTIME=1742351259556; JSESSIONID=8D2457473C1668B3E4288475DE1E24C2'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
