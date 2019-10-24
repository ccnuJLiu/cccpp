#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""使用requests请求代理服务器
请求http和https网页均适用
"""

import requests

# 要访问的目标网页
page_urls = ["https://www.linkedin.com/in/fang-chen-03630b2",
             #"https://www.baidu.com",
             #"https://www.sogou.com"
             ]

# 隧道服务器
tunnel_host = "tps136.kdlapi.com"
tunnel_port = "15818"

# 隧道id和密码
tid = "t17166103219953"
password = "jfix70w2"

proxies = {
        "http": "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port),
        "https": "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port),

    }

headers = {
    #"Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
    'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ch',
}

for url in page_urls:
    r = requests.get(url, proxies=proxies, headers=headers)


    print ('The status code is:', r.status_code)  # 获取Reponse的返回码
    print(r.content)

    if r.status_code == 200:
        r.enconding = "utf-8"  # 设置返回内容的编码
        print (r.content)  # 获取页面内容