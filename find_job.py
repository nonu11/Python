#!/usr/bin/env Python
#coding=utf-8
import re
import urllib.request
from bs4 import BeautifulSoup

def get_page(url):
    if url.find('jiuye.lut.cn') == -1:#返回值为-1则不含有该字段
        coding = 'utf-8'
    else:
        coding = 'gbk'
    result = urllib.request.urlopen(url)
    html = str(result.read(),coding)
    result.close()
    soup = BeautifulSoup(''.join(html),"html.parser")
    return soup.prettify()


def save_lut(html):
    msg = {}
    reg = r'<td style="line-height:24px;">(.*?)</td>'
    list = re.findall(reg,html,re.S|re.M)
    for i in list:
        re_t = r'<span class="blue">\n(.*?)</span>'
        re_h = r'<a href="(.*?)" target="_blank">'
        msglist = re.findall(re_t,i,re.S|re.M)
        hreflist = re.findall(re_h,i,re.S|re.M)
        msg.setdefault('时间',[]).append(msglist[0])
        msg.setdefault('单位',[]).append(msglist[1])
        msg.setdefault('地点',[]).append(msglist[2])
        msg.setdefault('简介',[]).append("http://jiuye.lut.cn/www/"+hreflist[0])
    for i in range(0,len(msg["时间"])):
        for j in msg:
            print(j+'：'+msg[j][i])
        print('------------------------------------------------------')

def save_jtu(html):
    msg = {}
    reg = r'<ul class="fl">(.*?)</ul>'
    list = re.findall(reg,html,re.S|re.M)
    for i in list:
        re_t = r'</span>\n(.*?)</li>'
        re_h = r'viewXjhxx\(\'(.*?)\'\)">'
        msglist = re.findall(re_t,i,re.S|re.M)
        hreflist = re.findall(re_h,i,re.S|re.M)
        msg.setdefault('时间',[]).append(msglist[0])
        msg.setdefault('单位',[]).append(msglist[1])
        msg.setdefault('地点',[]).append(msglist[2])
        msg.setdefault('简介',[]).append("http://jyzx.lzjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=viewXjhxx&id="+hreflist[0])
    for i in range(0,len(msg["时间"])):
        for j in msg:
            print(j+'：'+msg[j][i])
        print('------------------------------------------------------')

if __name__ == "__main__":
    url_jtu = "http://jyzx.lzjtu.edu.cn/eweb/jygl/index.so"
    url_lut = ["http://jiuye.lut.cn/www/ContentsMain.asp?Page=1&MainType=0&Keywords=&ClassId=27","http://jiuye.lut.cn/www/ContentsMain.asp?Page=2&MainType=0&Keywords=&ClassId=27"]
    print("兰州交通大学招聘信息\n")
    html = get_page(url_jtu)
    save_jtu(html)
    print("兰州理工大学招聘信息\n")
    for i in url_lut:
        html = get_page(url_jtu)
        save_jtu(html)
