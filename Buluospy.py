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
def random_string(randomlength=8,zero=False):
    chars='0123456789'
    length = len(chars)-1
    random = Random()

    if zero:
        randomlength--
        str = chars[random.randint(1,length)]

    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    
    return str

# 生成URL
def geturl(bid='22371',start=0):
    url='https://buluo.qq.com/cgi-bin/bar/post/get_post_by_page?bid='+bid+'&num=20&start='+str(start)+'&source=2&r=0.1'+random_string(17)+'&bkn='
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

# 获取Json
async def __fetch(sem,url,headers,loop):    
    try:
        async with sem:
            async with ClientSession(loop=loop) as session:
                async with session.get(url,data=None,headers=headers,timeout=5) as response:
                    return await response.json()
    except Exception as ex:
        print('_fetch Exception:%s'%ex)

# 获取发帖
async def getposts(bid='22371',loop=None):
    url = geturl(bid)
    headers = getheaders(bid)
    result = None

    # 限制并发数量
    sem = asyncio.Semaphore(20)

    try:
        # 先获取能访问到post数量
        gettotal_st = asyncio.ensure_future(__fetch(sem,url,headers,loop),loop=loop)
        gettotal_done = await asyncio.wait_for(gettotal_st,timeout=5)

        if 'retcode' not in gettotal_done or gettotal_done['retcode']!=0:
            print('This is bid[%s] get fail.'%bid)
            return result

        if 'total' not in gettotal_done['result']:
            print('bid[%s] can not get total.'%bid)
            return result

        total = gettotal_done['result']['total']

        # 获取所有post
        for i in range(0,total,20):
            pageurl = geturl(bid=bid,start=i)
            page_st = asyncio.ensure_future(__fetch(sem,pageurl,headers,loop),loop=loop)
            page_done = await asyncio.wait_for(page_st,timeout=5)    
            # 防止访问过于频繁导致的错误
            await asyncio.sleep(0.1)                    
    except Exception as ex:
        print('bid[%] getposts error:%s'%(bid,ex))