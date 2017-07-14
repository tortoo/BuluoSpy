# -*- coding: utf-8 -*-

import asyncio
from aiohttp import ClientSession
import aiomysql
import json
import pymysql
import time
from random import Random

# 把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(stamp))

# 随机数字字符串生成
def random_string(randomlength=8):
    str='0.'

    chars='0123456789'
    length = len(chars)-1
    random = Random()

    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    
    return str

# 生成URL
def geturl(bid='22371',start=0):
    url='https://buluo.qq.com/cgi-bin/bar/post/get_post_by_page?bid='+bid+'&num=20&start='+str(start)+'&source=2&r='+random_string(17)+'&bkn='
    return url

# 生成头
def getheaders(bid='22371'):
    headers ={
        'content-type':'application/json;charset=utf-8',
        'accept':'application/json',
        'accept-language':'zh-CN,zh;q=0.8',
        'Referer':'https://buluo.qq.com/p/barindex.html?bid='+bid,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
    }   
    return headers

# 获取实际发帖量
def getpostnum(bid='22371'):
    pass