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

# Example usage
encrypted_base64 = 'pi8qylupzSpl7TcVUO/mDteUAyht/2wn3CAVtfWhdTDOrqN0fbt/5I01DZylZ8dNB4EtpCSg2xEcl48IGe/KxA=='
aes_key_hex = '38613032663534626563383837353035'
aes_iv_hex = '31362d42797465732d2d537472696e67'

plaintext = decrypt_aes(encrypted_base64, aes_key_hex, aes_iv_hex)
print(plaintext)

encrypted_base64 = encrypt_aes(plaintext, aes_key_hex, aes_iv_hex)
print(encrypted_base64)






prefix = "dx-"
suffix = "-1"

random_number_1 = str(random.randrange(1000000000000, 10000000000000))
random_number_2 = str(random.randrange(1000000, 10000000))

result = prefix + random_number_1 + "-" + random_number_2 + suffix
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
}

# ?w=315&h=150&s=50&ak=dd070b0b9ba2ffa81d655c0f492ef2e0&c=67d00270rJSOBsYbshD5jBXkevqUakFuxRwjiGB1&jsv=1.3.41.439&aid=dx-1741750144180-5376685-2&
# wp=1&de=0&uid=&lf=0&tpc=&isDark=false&_r=0.39247413367079376

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
response = requests.get('https://captcha.vivo.com.cn/api/a', headers=headers, params=params).json()
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

p1_img = requests.get(p1_url)
p2_img = requests.get(p2_url)

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

code = '''
    let input = document.querySelector('input[placeholder="请输入手机号"]');
    if (input) {
        input.value = "13800138000";
        input.dispatchEvent(new Event('input', { bubbles: true }));
        let btn = document.querySelector('.get-code-pc .get');
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
response = requests.post(url, data=data)
token = response.json()['token']




data = {
    'phone': '17381560710',
    'areaCode': '86',
    'ticket': '',
    'randomNum':'',
    'client_id': '131',
    '_isSafe_': 'true',
    'sliderVersionType': '2',
    'clientType':'2',
    'countryCode': 'CN',
    'deviceType':'wap',
    "timeStamp": str(int(time.time() * 1000)),  # 当前时间戳（毫秒
    "nounce": "1421048d1a0071d89d3bca6b1e8067a3de7861b3bde7c11ded45116938696685",
    "locale": "zh_CN",
    "authcookie": "3",
    'e':3,
    'msminv':'25012200',
    "ticket": f"{token}:67cff457cSxVESQs6l2MFTEgVbLK7jo5EuHvFx91",
    'constID':'CID:1741766337746',
}

query_string = urlencode(data)
cipher_text = encrypt_aes(query_string, aes_key_hex, aes_iv_hex)
encrypted_data = base64.b64decode(cipher_text)
encData = encrypted_data.hex()


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

payload = f"encData={encData}&encKey={encKey}&encVer=1_1_3"

url = 'https://passport.vivo.com.cn/v5/smsLogin/p1'
res = requests.post(url, data=data, headers=headers)
print(res.text)



