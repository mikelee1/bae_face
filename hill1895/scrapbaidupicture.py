#!/usr/bin/env python
# encoding=utf-8

import urllib, urllib2, cookielib, re, sys, threading,time

# myemail = '1430086923@qq.com'
# mypassword = 'renren1212'

# req = urllib2.Request(
#     'http://www.renren.com/PLogin.do',
#
# )
#
# cj = cookielib.LWPCookieJar()
#
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# urllib2.install_opener(opener)
# r = opener.open(req)
# tmp = r.read()
# self.myid = re.search(r'http://www.renren.com/(\d+)', tmp).group(1)
opener = urllib.urlopen('http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gbk&word=%B6%AF%CE%EF%C1%B3%B2%BF%CD%BC%C6%AC%20%CF%C2%D4%D8&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=000000')
html = opener.read()
print(html)