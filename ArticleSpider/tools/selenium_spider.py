#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Liang'

from selenium import webdriver
from scrapy.selector import Selector

# browser = webdriver.Chrome(executable_path="/home/drjr/chromedriver/chromedriver")

# 知乎模拟登陆
# browser.get("https://www.zhihu.com/#/signin")
#
# browser.find_element_by_css_selector(".SignFlow-account input[type='text']").send_keys("")
# browser.find_element_by_css_selector(".SignFlow-password input[type='password']").send_keys("")
# browser.find_element_by_css_selector(".Login-content button[type='submit']").click()

# 提取淘宝页面加个
# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tb-property-cont .tb-rmb-num::text").extract())


# selenium 模拟登陆微博
# browser.get("https://www.weibo.com")
#
# import time
# time.sleep(15)
#
# browser.find_element_by_css_selector("#loginname").send_keys("***")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("***")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
#
# browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")


# selenium 模拟开源中国博客网鼠标下拉
# browser.get("http://www.oschina.net/blog")
#
# import time
# time.sleep(5)
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
#     time.sleep(2)


# 设置chrome不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_opt.add_experimental_option("prefs", prefs)
#
# browser = webdriver.Chrome(executable_path="/home/drjr/chromedriver/chromedriver", chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")

# phantomjs, 无界面浏览器, 多进程情况下, phantomjs 性能下降严重
# browser = webdriver.PhantomJS(executable_path="/home/drjr/phantomjs/phantomjs")
# browser.get("https://www.taobao.com/markets/tbhome/yhh-detail?spm=a21bo.2017.201870.3.7872de06Fgn8fH&contentId=2500000200478361072&scm=1007.12846.65991.0&pvid=b9980731-1685-4ea8-a1d4-f4b51392e7d0")
#
# print(browser.page_source)
# browser.quit()  # phantomjs 看不见界面, 所以记住要程序退出


# python 自带无界面操作方法
# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(800, 600))
# display.start()
# browser = webdriver.Chrome()
# browser.get("www.baidu.com")
# print(browser.page_source)
