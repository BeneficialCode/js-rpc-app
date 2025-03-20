import blackboxprotobuf

with open('_tmp_bak','rb') as f:
    data = f.read()

deserial_data,message_type = blackboxprotobuf.protobuf_to_json(data)
print(deserial_data)
print(message_type)

def get_cookie_value(cookie_str, key):
    cookies = cookie_str.split("; ")
    for cookie in cookies:
        k, v = cookie.split("=", 1)  # 只分割一次，避免值中有 "=" 导致错误
        if k == key:
            return v
    return None

cookie_str = "smidV2=202503111729078de7304017b1b31da09208dffcb9db90001f2d4d4b66c4f00; _dx_uzZo5y=d05353d5990ffae46327b0d94b1d6208ae5f8eda1594358d63a0f136b93ce3f55e2135b1; cookieId=d9877fcc-d5fb-cd16-34f7-bb164c69c4001741685516388; Hm_lvt_9ef7debb81babe8b94af7f2c274869fd=1741685516,1741685767; _dx_app_dd070b0b9ba2ffa81d655c0f492ef2e0=67da920ddf9WzZqdUBG0WSifCyrjSXYQrOKxXea1; _dx_captcha_vid=195ADCF4649DD070B0B9B17109A9F847344C59FB3471CD2F1AE63; language=zh_CN; .thumbcache_77352f771aaa31eaeebd60722ce25500=P43+4ILbkZGB8PQ67OuoPCIMYX348lqxr77M7ErskWHJOMPSG+pcvAJsxWOM/OHRHFEHZGc4uE3ZZKUXYj+nPA%3D%3D"

print(get_cookie_value(cookie_str, "language"))  # 输出: zh_CN
print(get_cookie_value(cookie_str, "smidV2"))  # 输出: 202503111729078de7304017b1b31da09208dffcb9db90001f2d4d4b66c4f00
