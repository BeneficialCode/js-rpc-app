import requests

code = ''

with open('baseutil.js','r',encoding='utf-8') as f:
    code = f.read()

call_str = '''
encryptAES("123456")'''

code += call_str
import requests


url = "http://localhost:12080/execjs"
data = {
    "group": "rpc",
    "code": code
}
res = requests.post(url, data=data)
print(res.text)
