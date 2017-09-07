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
    data = open('lut_job.txt', 'ab+')
    msg = {}
    reg = r'<td style="line-height:24px;">(.*?)</td>'
    list = re.findall(reg,html,re.S|re.M)
    for i in list:
        re_t = r'<span class="blue">\n\s+(.*?)</span>'
        re_h = r'<a href="(.*?)" target="_blank">'
        msglist = re.findall(re_t,i,re.S|re.M)
        hreflist = re.findall(re_h,i,re.S|re.M)
        msg.setdefault('时间',[]).append(msglist[0])
        msg.setdefault('单位',[]).append(msglist[1])
        msg.setdefault('地点',[]).append(msglist[2])
        msg.setdefault('简介',[]).append("http://jiuye.lut.cn/www/"+hreflist[0])
    for i in range(0,len(msg["时间"])):
        for j in msg:
            s = j+'：'+msg[j][i]
            data.write(('\r\n'+s+'\r\n').encode())
            print(s)
        data.write('\r\n------------------------------------------------------\r\n'.encode())
        print('\n------------------------------------------------------\n')
    data.close()

def save_jtu(html):
    data = open('jtu_job.txt', 'w')
    msg = {}
    reg = r'<div class="z_newsl">(.*?)</ul>'
    list1 = re.findall(reg,html,re.S|re.M)
    #print(list1)
    res = r'<li>(.*?)</li>'
    list = re.findall(res,str(list1),re.S|re.M)
    for i in list:
        re_d = r'<div style="text-align:center;float: left;width: 90px;">\\n\s+(.*?)\\n'
        re_t = r'<div style="text-align:center;float: left;width: 100px;">\\n\s+(.*?)\\n'
        re_a = r'<div style="text-align:left;float: left;width: 180px;">\\n\s+(.*?)\\n'
        re_c = r'onclick="viewXphxx.*?">\\n\s+(.*?)\\n'
        re_l = r'onclick="viewXphxx\(\\\'(.*?)\\\'\)'
        datelist = re.findall(re_d,i,re.S|re.M)
        timelist = re.findall(re_t,i,re.S|re.M)
        addresslist = re.findall(re_a,i,re.S|re.M)
        complist = re.findall(re_c,i,re.S|re.M)
        linklist = re.findall(re_l,i,re.S|re.M)
        msg.setdefault('时间',[]).append(datelist[0]+"  "+timelist[0])
        msg.setdefault('单位',[]).append(complist[0])
        msg.setdefault('地点',[]).append(addresslist[0])
        msg.setdefault('简介',[]).append("http://jyzx.lzjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=viewXjhxx&id="+linklist[0])
    for i in range(0,len(msg["时间"])):
        for j in msg:
            s = j+'：'+msg[j][i]
            data.write(('\n'+s+'\n'))
            print(s+'\n')
        data.write('\n---------------------------------------------------------\n')
        print('-------------------------------------------------------\n')
    data.close()

if __name__ == "__main__":
    url_jtu = "http://jyzx.lzjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=all"
    url_lut = ["http://jiuye.lut.cn/www/ContentsMain.asp?Page=1&MainType=0&Keywords=&ClassId=27","http://jiuye.lut.cn/www/ContentsMain.asp?Page=2&MainType=0&Keywords=&ClassId=27"]
    print("兰州交通大学招聘信息\n")
    html = get_page(url_jtu)
    save_jtu(html)
    print("兰州理工大学招聘信息\n")
    for i in url_lut:
        html = get_page(i)
        save_lut(html)
