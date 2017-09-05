# ！bin/usr/python/bin
# _*_coding_*_:utf-8

import socket
import threading
import time

socket.setdefaulttimeout(3)
mlock = threading.RLock()

def socket_port(ip, port):
    try:
        if port >= 65535:
            print(u"端口扫描结束 0-65535")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if (result == 0):
            mlock.acquire() #加锁
            print(ip, u":", port, u"端口开放")
            mlock.release() #释放锁
        s.close()
    except:
        print(u"异常2")


def ip_port(data):
    try:
        t = time.time()
        for i in range(80, 65535):
            threading.Thread(target=socket_port(data, int(i))).start()
        print(u"扫描端口完成用时 time:%f" % (time.time() - t))
    except:
        print(u"异常1")


if __name__ == '__main__':
    ip_port("127.0.0.1")
