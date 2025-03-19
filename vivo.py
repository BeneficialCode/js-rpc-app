import requests
import random
import ddddocr
from PIL import Image
from io import BytesIO
from PIL import Image
import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
from Crypto.Util.Padding import pad
from urllib.parse import urlencode
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import binascii
import urllib.parse
import cv2
import numpy as np
import hashlib

def decrypt_aes(encrypted_base64, aes_key_hex, aes_iv_hex):
    """
    Decrypts an AES-encrypted base64 string using the provided key and IV in hex format.

    :param encrypted_base64: The base64 encoded encrypted data.
    :param aes_key_hex: The AES key in hex format.
    :param aes_iv_hex: The AES IV in hex format.
    :return: The decrypted plaintext string.
    """
    # Convert hex strings to bytes
    aes_key = bytes.fromhex(aes_key_hex)
    aes_iv = bytes.fromhex(aes_iv_hex)

    # Decode the base64 encoded encrypted data
    encrypted_data = base64.b64decode(encrypted_base64)

    # Create AES cipher object
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    plaintext = decrypted_data.decode('utf-8')
    return plaintext

def encrypt_aes(plaintext, aes_key_hex, aes_iv_hex):
    """
    Encrypts a plaintext string using AES encryption with the provided key and IV in hex format.

    :param plaintext: The plaintext string to encrypt.
    :param aes_key_hex: The AES key in hex format.
    :param aes_iv_hex: The AES IV in hex format.
    :return: The base64 encoded encrypted data.
    """
    # Convert hex strings to bytes
    aes_key = bytes.fromhex(aes_key_hex)
    aes_iv = bytes.fromhex(aes_iv_hex)

    # Create AES cipher object
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    # Pad the plaintext and encrypt
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted_data = cipher.encrypt(padded_plaintext)

    # Encode the encrypted data to base64
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_base64

session = requests.session()

# Example usage
encrypted_base64 = 'pi8qylupzSpl7TcVUO/mDteUAyht/2wn3CAVtfWhdTDOrqN0fbt/5I01DZylZ8dNB4EtpCSg2xEcl48IGe/KxA=='
aes_key_hex = '63346135363163366634653461643237'
aes_iv_hex = '31362d42797465732d2d537472696e67'

# plaintext = decrypt_aes(encrypted_base64, aes_key_hex, aes_iv_hex)
# print(plaintext)

plaintext = 'sliderVersionType=2&constID=CID%3A1741832695857&imei=&randomNum=8ad51235cccbe1d7&phone=18483517021&areaCode=86&ticket=1958D51B011DD070B0B9B78C05D6B44E4405C81964A72E6379B0E%3A67cff457cSxVESQs6l2MFTEgVbLK7jo5EuHvFx91&client_id=131&countryCode=CN&deviceType=pc&timeStamp=1741832695858&nounce=88abd8330b0cc5558c10bc258f99a9597b1ae960a2552ac5a8e8eb93d603b532&locale=zh_CN&authcookie=1&e=3&msminv=25012200'
encrypted_base64 = encrypt_aes(plaintext, aes_key_hex, aes_iv_hex)
encrypted_data = base64.b64decode(encrypted_base64)
encData = encrypted_data.hex()
print(encData)


prefix = "dx-"
suffix = "-1"

random_number_1 = str(random.randrange(1000000000000, 10000000000000))
random_number_2 = str(random.randrange(1000000, 10000000))

result = prefix + random_number_1 + "-" + random_number_2 + suffix
headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'Connection': 'keep-alive',
  'Origin': 'https://passport.vivo.com.cn',
  'Referer': 'https://passport.vivo.com.cn/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Cookie': 'vivo_account_cookie_iqoo_deviceid=wb_df91d702-0a10-4756-a6a0-e9c044096592'
}

params = (
    ('w', '288'),
    ('h', '144'),
    ('s', '50'),
    ('ak', 'dd070b0b9ba2ffa81d655c0f492ef2e0'),
    ('c', '67d00270rJSOBsYbshD5jBXkevqUakFuxRwjiGB1'),
    ('jsv', '1.3.41.439'),
    ('aid', result),
    ('wp', '1'),
    ('de', '0'),
    ('uid', ''),
    ('lf', '0'),
    ('tpc', ''),
    ('isDark', 'false'),
    ('wtf', 'false'),
    ('_r', '0.39247413367079376'),
)

# https://captcha.vivo.com.cn/api/a
response = session.get('https://captcha.vivo.com.cn/api/a', headers=headers, params=params).json()
o = response["o"]
sid=response["sid"]
url = response["p1"]
hk=response["p2"]
y=response["y"]

p1_url = "https://captcha.vivo.com.cn" + url
p2_url = "https://captcha.vivo.com.cn" + hk

code = ''
with open('dingxiang_oppo.js','r',encoding='utf-8') as f:
    code = f.read()
call_str = f'''
get_img('{o}')'''

code += call_str
url = "http://localhost:12080/execjs"
data = {
    "group": "rpc",
    "code": code
}
res = requests.post(url, data=data)
json_data = res.json()
arr = json_data['data']
arr = eval(arr)

p1_img = session.get(p1_url)
p2_img = session.get(p2_url)

p1_img_data = BytesIO(p1_img.content)

org_img_file = Image.open(p1_img_data)

new_img_file = Image.new('RGB',(400,200))

for index in range(len(arr)):
    c = arr[index] * 12
    l = org_img_file.crop((c, 0, c + 12, 200))

    new_x = index * 12
    new_img_file.paste(l,(new_x,0))

new_img_file.paste(org_img_file.crop((384,0,400,200)),(384,0))
output = BytesIO()
new_img_file.save("output.jpg")
new_img_file.save(output, format='JPEG')

ocr = ddddocr.DdddOcr(det=False,ocr=False)

target_bytes = p2_img.content

with open('output.jpg','rb') as f:
    backgroud_bytes = f.read()

res = ocr.slide_match(target_bytes,backgroud_bytes,simple_target=True)
x = res["target"][0]

x = int(x/400*288)

code = '''
    window.location.href = "https://passport.vivo.com.cn/#/login";
'''
data['code'] = code
res = requests.post(url, data=data)
print(res.text)

time.sleep(3)

code = '''
    var input = document.querySelector('input[placeholder="请输入手机号"]');
    if (input) {
        input.value = "13800138000";
        input.dispatchEvent(new Event('input', { bubbles: true }));
        var btn = document.querySelector('.get-code-pc .get');
        if (btn) {
            btn.click();
        }
    }
'''
data['code'] = code
res = requests.post(url, data=data)
print(res.text)


with open('ac.js','r',encoding='utf-8') as f:
    code = f.read()

code += f'''
    get_actoken({x},{y},'{sid}')
'''

data['code'] = code
res = requests.post(url, data=data)
json_data = res.json()
ac = json_data['data']


js_code = '''
    window.localStorage.getItem("smDeviceId")
'''
url = "http://localhost:12080/execjs"
data = {
    "group": "rpc",
    "code": js_code
}
res = requests.post(url, data=data)
smDeviceId = res.json()['data']

headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'Connection': 'keep-alive',
  'Content-type': 'application/x-www-form-urlencoded',
  'Origin': 'https://passport.vivo.com.cn',
  'Referer': 'https://passport.vivo.com.cn/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Cookie': 'vivo_account_cookie_iqoo_deviceid=wb_df91d702-0a10-4756-a6a0-e9c044096592'
}

url = "https://captcha.vivo.com.cn/api/v1"
data = {
    "ac": ac,
    "ak": "dd070b0b9ba2ffa81d655c0f492ef2e0",
    "c": "67cff457cSxVESQs6l2MFTEgVbLK7jo5EuHvFx91",
    "jsv": "1.3.41.439",
    "sid": sid,
    "aid": "dx-1741767808896-99701937-2",
    "x":x,
    "y":y
}
response = session.post(url, data=data,headers=headers)
print(response.text)
token = response.json()['token']

url = "http://localhost:12080/execjs"
aes_key = bytes.fromhex(aes_key_hex).decode("utf-8")
code = f'''
JSEncrypt.encrypt('{aes_key}','MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgF21fulwAZs3l6ru8M2fLPDO9Y4+0zOF0Dblz7nOmrGYGDIpcPwegNYLvpQrcFq2YjfCzVF+n1xd+k8hiYxdwggp9oiB9UCN4MLr+qOZXtWKxBJDQAOn3w+tu0SwGwKsONI+CDGtF5l5yfjAunTYwLduc3aqZjPmo2UXbGdGqrGbxPS5lY3/kZykce+i+txO7vYfJevHYyg5eaOGfpjN8/666L60mv+Xpqd272c3VcbjbYW5ZJCljhZnHR+cPeAyn6P5encb0afQhoyz0LnARiRP51C9Nv4avG/RbGgD2o4asbaEXJ6zPgDxRE4e34EkhGM46XcmmJeQSA54LSJ43QIDAQAB')
'''
data = {
    "group": "rpc",
    "code": code
}
res = requests.post(url, data=data)
encKey = res.json()['data']
encKey = urllib.parse.quote(encKey)

cid = str(int(time.time() * 1000))
timeStamp = str(int(time.time() * 1000))
nounce = hashlib.md5(timeStamp.encode('utf-8')).hexdigest()

data = {
    'phone': '18483517020',
    'areaCode': '86',
    'ticket': '',
    'randomNum': '',
    'client_id': '',
    '_isSafe_': 'true',
    'sliderVersionType': '2',
    'clientType': '2',
    'countryCode': 'CN',
    'deviceType': 'pc',
    'timeStamp': timeStamp,
    'nounce': '808c7b4da0c575ba5b180834ef7b496b97c85249ee231859af733d8a17afb173',
    'locale': 'zh_CN',
    'authcookie': '1',
    'e': '3',
    'msminv': '25012200'
}

query_string = urlencode(data)
cipher_text = encrypt_aes(query_string, aes_key_hex, aes_iv_hex)
encrypted_data = base64.b64decode(cipher_text)
encData = encrypted_data.hex()

payload = f"encData={encData}&encKey={encKey}&encVer=1_1_2"

url = "https://passport.vivo.com.cn/v5/smsLogin/p1"
response = session.post(url, data=payload, headers=headers)
cipher_text = response.text[4:]
cipher_text = bytes.fromhex(cipher_text)
cipher_text_b64 = base64.b64encode(cipher_text)
plaintext = decrypt_aes(cipher_text_b64, aes_key_hex, aes_iv_hex)

json_data = json.loads(plaintext)
randomNum = json_data['data']['randomNum']


cid = str(int(time.time() * 1000))
timeStamp = str(int(time.time() * 1000))
nounce = hashlib.md5(timeStamp.encode('utf-8')).hexdigest()


data = {
    'phone': '18483517020',
    'areaCode': '86',
    'randomNum':randomNum,
    'client_id': '131',
    'sliderVersionType': '2',
    'countryCode': 'CN',
    'deviceType':'pc',
    'constID':f'CID:{cid}',
    "timeStamp": timeStamp,  # 当前时间戳（毫秒
    "nounce": nounce,
    "locale": "zh_CN",
    "authcookie": "1",
    'e':3,
    'msminv':'25012200',
    "ticket": f"{token}:67cff457cSxVESQs6l2MFTEgVbLK7jo5EuHvFx91",
}

query_string = urlencode(data)
cipher_text = encrypt_aes(query_string, aes_key_hex, aes_iv_hex)
encrypted_data = base64.b64decode(cipher_text)
encData = encrypted_data.hex()



payload = f"encData={encData}&encKey={encKey}&encVer=1_1_2"

url = 'https://passport.vivo.com.cn/v5/smsLogin/p1'



headers = {
  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
}

headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
  'Origin': 'https://passport.vivo.com.cn',
  'Referer': 'https://passport.vivo.com.cn/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Cookie': 'vivo_account_cookie_iqoo_deviceid=wb_df91d702-0a10-4756-a6a0-e9c044096592'
}
res = session.post(url, data=payload, headers=headers)
print(res.text)
cipher_text = res.text[4:]
cipher_text = bytes.fromhex(cipher_text)
cipher_text_b64 = base64.b64encode(cipher_text)
plaintext = decrypt_aes(cipher_text_b64, aes_key_hex, aes_iv_hex)
print(plaintext)



# do login
code = input('请输入验证码：')
timeStamp = str(int(time.time() * 1000))
nounce = hashlib.md5(timeStamp.encode('utf-8')).hexdigest()



data = {
    "phone": "18483517020",
    "areaCode": "86",
    "code": code,
    "remember": "0",
    "client_id": "131",
    "redirect_uri": "https://pc.vivo.com.cn/suite?origin=cloudWeb",
    "alreadySendCode": "1",
    "bizCode": "BC0063",
    "supportReplay": "1",
    "smDeviceId": smDeviceId,
    "countryCode": "CN",
    "deviceType": "pc",
    "timeStamp": timeStamp,
    "nounce": nounce,
    "locale": "zh_CN",
    "authcookie": "1",
    "e": "3",
    "msminv": "25012200"
}

query_string = urlencode(data)
cipher_text = encrypt_aes(query_string, aes_key_hex, aes_iv_hex)
encrypted_data = base64.b64decode(cipher_text)
encData = encrypted_data.hex()

url = "https://passport.vivo.com.cn/v5/smsLogin/p2"

payload = f"encData={encData}&encKey={encKey}&encVer=1_1_2"

response = session.post(url, data=payload, headers=headers)
print(response.text)
cipher_text = response.text[4:]
cipher_text = bytes.fromhex(cipher_text)
cipher_text_b64 = base64.b64encode(cipher_text)
plaintext = decrypt_aes(cipher_text_b64, aes_key_hex, aes_iv_hex)
print(plaintext)

url = 'https://passport.vivo.com.cn/v3/web/login/authorize?client_id=9&redirect_uri=https://webcloud.vivo.com.cn/login&response_type=code&page_type=0'
response = session.get(url, headers=headers)
redirect_url = response.headers.get('Location')
response = session.get(redirect_url, headers=headers)

url = f'https://webcloud.vivo.com.cn/queryaccount?_t={int(time.time() * 1000)}'
response = session.get(url, headers=headers)
print(response.text)

url = f'https://webcloud.vivo.com.cn/secondCheck/checkIfTrustDevice?from=findphone&_t={int(time.time() * 1000)}'
response = session.get(url, headers=headers)
print(response.text)




