#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Liang'


import requests
from scrapy.selector import Selector
import MySQLdb

# conn = MySQLdb.connect(host="***", port=***, user='***', passwd='***', db='***', charset="utf8")
# cursor = conn.coursor()


class GetIP(object):
    def judge_ip(self, ip, port):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        proxy_dict = {
            "http": proxy_url
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            # print("invalid ip and port")
            return False
        else:
            code = response.status_code
            if code >= 200 and not code >= 300:
                print("effective ip")
                print(ip)
                return True
            else:
                # print("invalid ip and port")
                return False


def crawl_ips():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36"}

    getip_obj = GetIP()

    for i in range(2049):
        re = requests.get("https://www.kuaidaili.com/free/inha/{0}/".format(i), headers=headers)
        print(re.status_code)
        if re.status_code >=200 and not re.status_code > 300:
            print(i)

            selector = Selector(text=re.text)
            all_trs = None
            all_trs = selector.css("#list tbody tr")

            ip_list = []
            for tr in all_trs:
                speed_str = tr.css('td[data-title="响应速度"]::text').extract()[0]
                if speed_str:
                    speed = float(speed_str.split('秒')[0])

                all_text = tr.css("td::text").extract()

                # print(all_text)

                ip = all_text[0]
                port = all_text[1]
                proxy_type = all_text[2]

                print(ip)

                judge_re = getip_obj.judge_ip(ip, port)
                if judge_re:
                    return "http://{0}:{1}".format(ip, port)

                # ip_list.append((ip, port, proxy_type, speed))

# print(crawl_ips())
