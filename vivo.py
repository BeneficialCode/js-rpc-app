import requests
import random
import ddddocr
import execjs
from PIL import Image
from io import BytesIO
from PIL import Image

prefix = "dx-"
suffix = "-1"

random_number_1 = str(random.randrange(1000000000000, 10000000000000))
random_number_2 = str(random.randrange(1000000, 10000000))

result = prefix + random_number_1 + "-" + random_number_2 + suffix
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
}

params = (
    ('w', '288'),
    ('h', '144'),
    ('s', '50'),
    ('ak', '9624bfa96b3675a4b8f27b683882e15f'),
    ('c', '658cee79DrNFIXLYJV5RkG7B4vOzlA6yFhuQYLz1'),
    ('jsv', '1.3.41.439'),
    ('aid', result),
    ('wp', '1'),
    ('de', '0'),
    ('uid', ''),
    ('lf', '0'),
    ('tpc', ''),
    ('isDark', 'false'),
    ('wtf', 'false'),
    ('_r', '0.6218359241176445'),
)

response = requests.get('https://captcha-sec.heytapmobi.com/api/a', headers=headers, params=params).json()
o = response["o"]
sid=response["sid"]
url = response["p1"]
hk=response["p2"]
y=response["y"]

p1_url = "https://captcha-sec.heytapmobi.com" + url
p2_url = "https://captcha-sec.heytapmobi.com" + hk

code = ''
with open('dingxiang_oppo.js','r',encoding='utf-8') as f:
    code = f.read()
call_str = f'''
return get_img('{o}')'''

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


