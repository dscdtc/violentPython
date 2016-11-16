# -*- coding:utf-8 -*-
__author__ = 'dscdtc'

import zipfile
import optparse #定义命令行参数
from threading import Thread

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print '[+] Found Password \'%s\'' % password
        exit(0)
        return password
    except:
        return #pass

def main():
    #创建OptionParser对象；定义命令行参数;调用parse_args()解析命令行
    usage = "%prog -f <zipfile> -d <dictionary>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-f', dest='zname', type='string',\
                    help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
                    help='specify dictionary file')
    (options, args) = parser.parse_args()

    #按位或运算判断flags是否为空
    if (options.zname == None) | (options.dname == None):
        print parser.print_help()
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)
    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()

if __name__ == '__main__':
    main()
