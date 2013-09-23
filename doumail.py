#!/usr/bin/env python
#--coding: utf-8--
__author__ = 'tea'

import time
import os
import re
import urllib
import urllib2
import cookielib
from data_mongo import MongoCRUD
import time
import sys

loginurl = 'https://www.douban.com/accounts/login'
cookie = cookielib.LWPCookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), urllib2.HTTPHandler) #cookie
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
params = {
    "form_email": "jijiagogo@163.com",
    "form_password": "xianchang123",
    "source": "index_nav" #没有的话登录不成功
}
#参数reporthook是一个回调函数，当连接上服务器、以及相应的数据块传输完毕的时候会触发该回调。我们可以利用这个回调函 数来显示当前的下载进度
def cbk(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per
#从首页提交登录
def doubanLogin():
    response = opener.open(loginurl, urllib.urlencode(params))

    #验证成功跳转至登录页
    if response.geturl() == "https://www.douban.com/accounts/login":
        html = response.read()

    # cookie = cookielib.MozillaCookieJar()
    #登录
    response = opener.open(loginurl, urllib.urlencode(params))
    #验证成功跳转至登录页
    if response.geturl() == "https://www.douban.com/accounts/login":
        html = response.read()
    #验证码图片地址
        imgurl = re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
        if imgurl:
            print 'imgurl', imgurl
            url = imgurl.group(1)
            #将图片保存至同目录下
            print 'url1', url
            res = urllib.urlretrieve(url, 'tee.jpg', cbk)
            #获取captcha-id参数
            captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            if captcha:
                vcode = raw_input(u'请输入图片上的验证码：')
                params["captcha-solution"] = vcode
                params["captcha-id"] = captcha.group(1)
                params["user_login"] = "登录"
                #提交验证码验证
                response = opener.open(loginurl, urllib.urlencode(params))  #将dict或者包含两个元素的元组列表转换成url参数。例如 字典{'name': 'dark-bull', 'age': 200}将被转换为"name=dark-bull&age=200"
                ''' 登录成功跳转至首页 '''
                if response.geturl() == "http://www.douban.com/":
                    print 'login success !'
                    #focusList()
                    #sendDouYou(10000000)
                else:
                    print 'login failed,you may enter the wrong code!'
        else:
            print 'error'
        #发豆邮 只要收件人是存在正确的id就能发豆邮 不是只能发给关注的人


def sendDouYou(Uid):
    for i in range(0,len(Uid)):
        uid = Uid[i]
        try:
            sendYou = 'http://www.douban.com/doumail/write?to=%s' % uid
            print 'sendYou', sendYou

            p = {"ck": ""}
            # print '---cookie---', cookie._normalized_cookie_tuples , type(cookie._normalized_cookie_tuples)
            c = [c.value for c in list(cookie) if c.name == 'ck']
            if len(c) > 0:
                p["ck"] = c[0].strip('"')
                # res=opener.open(sendYou)
            # html = res.read()
            filename = str(i%10) + '.txt'
            f = open(filename)
            base_text = f.read()
            text = 'hello ' + uid +' ,我跟你说： ' + base_text
            # text  = base_text
            f.close()
            p["m_text"] = text
            p["m_submit"] = '好了，寄出去'
            p['to'] = uid
            request=urllib2.Request(sendYou)
            # request=urllib2.Request(addtopicurl)
            request.add_header("User-Agent","Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130625 Firefox/17.0")
            request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
            request.add_header("Origin", "http://www.douban.com")
            request.add_header("Referer", sendYou)
            ('Content-Type','application/x-www-form-urlencoded')
            opener.open(request, urllib.urlencode(p))
            print time.ctime(),'豆邮发成功成功'
        except Exception, e:
            print 'error---------------------------------------\n',e
        print '*******************休息10分钟再继续发豆邮******************'
        time.sleep(600)


if __name__ == '__main__':

    data = MongoCRUD()
    UID = data.get_UID()
    UID=list(set(UID))  #OR UID = {}.fromkeys(UID).keys()删除list中重复的值
    # UID = ['3239220', '53932283', 'liull600', '53482702', '77569669', '77569262', 'alice851024', 'whyowhy', '59777334']
    print type(UID),len(UID)
    print UID
    # UID = [77139126,59571335,78086407]
    # 59571335 #白图先生的UID号码
    # 78086407 #Trina的UID号码
    doubanLogin()
    # aimee给其他用户发豆邮
    sendDouYou(UID)
    #白兔先生UID：59571335
    #aimee UID: 77139126
