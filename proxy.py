#! /usr/bin/python
# coding='utf-8'
"""
Author: zhouzying
URL: www.zhouzying.cn
Data: 2018-11-11
"""
import requests
from bs4 import BeautifulSoup
import re
import http.client


def get_proxy():
    """
    获取代理列表
    :return: proies
    """
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    # url = 'http://www.xicidaili.com/'
    # 国内高代理
    url = 'http://www.xicidaili.com/nn/1'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html5lib')
    # table = soup.find('table', attrs={'id': 'ip_list'})

    # 提取ip
    proies = []
    for tr in soup.table.tbody.find_all_next('tr'):
        items = {}
        # 提取ip
        ip_pattern = "<td>(\d+.\d+.\d+.\d+)</td>"
        ip = re.findall(ip_pattern, str(tr))
        if len(ip) == 0:
            pass
        else:
            items['ip'] = ip[0]

            # 提取端口号
            port_pattern = "<td>(\d+)</td>"
            port = re.findall(port_pattern, str(tr))
            items['port'] = port[0]
            # print(port)
            # 提取协议
            scheme_pattern = "<td>(HTTPS?)</td>"
            scheme = re.findall(scheme_pattern, str(tr))
            items['scheme'] = str(scheme[0]).lower()
            # print(scheme)
            proies.append(items)
    return proies


def verifyproxy(proxies):
    """
    验证代理的有效性
    :param proxies:
    :return:
    """
    url = "http://www.baidu.com"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    for item in proxies:
        ip = item['ip']
        port = item['port']
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
            conn.request(method='GET', url=url, headers=headers)

            print("代理可用:{}:{}".format(ip, port))

        # 请求出现异常
        except:
            print("代理不可用:{}:{}".format(ip, port))


proxies = get_proxy()
verifyproxy(proxies)
