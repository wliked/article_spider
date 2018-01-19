#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Liang'


import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com",
    "User-Agent":agent
}


def is_login():
    setting_url = "https://www.zhihu.com/settings/profile"
    response = session.get(setting_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    text = response.text
    print(text)
    temp_text = "xsrf&quot;:"
    str_index = text.find(temp_text)
    text2 = text[str_index:str_index+60]

    match_obj = re.match("xsrf.*quot;(.*?)&quot", text2)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print('ok')


def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open("captcha.jpg")
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")
    return captcha


def zhihu_login(account, password):
    if re.match("^1\d{5,10}", account):
        print('手机号码登陆')
        post_url = "https://www.zhihu.com/login/phone_num"
        # post_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }

        response_text = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()

zhihu_login("***", "***")
# get_index()
# is_login()
# get_captcha()