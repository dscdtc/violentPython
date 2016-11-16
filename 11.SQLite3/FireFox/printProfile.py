# -*- coding:utf-8 -*-
__author__ = 'dscdtc'

import os
import re
import sqlite3
import optparse

def printDownloads(downloadDB):
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    c.execute("SELECT name, source, datetime(endTime/1000000,\
            \'unixepoch\') FROM moz_downloads;"
            )
    print '\n[*]   --- Files Downloaded --- '
    for row in c:
        print '[+] File: %s from source: %s at: %s ' % \
            (row[0], row[1], row[2])
    conn.close()

def printCookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies')
        print '\n[*] -- Found Cookies -- '
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print '[+] Host: %s, Cookies: %s, Value: %s' % \
                (host, name, value)
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your cookies database.'
            print '[*] Upgrade your Python-Sqlite3 Library'
            exit(0)
    finally:
        conn.close()

def printHistory(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute("SELECT url, datetime(visit_date/1000000, \
            \'unixepoch\') FROM moz_places, moz_historyvisits \
            WHERE visit_count > 0 AND moz_places.id==\
            moz_historyvisits.place_id;")
        print '\n[*] -- Found History -- '
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print '[+] %s - Visited: %s' % (date, url)
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your cookies database.'
            print '[*] Upgrade your Python-Sqlite3 Library'
            exit(0)
    finally:
        conn.close()

def printBaidu(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date/1000000, \
        \'unixepoch\') FROM moz_places, moz_historyvisits \
        WHERE visit_count > 0 AND moz_places.id==\
        moz_historyvisits.place_id;")
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'baidu' in url.lower():
            r = re.findall(r'wd=.*\&', url)
            search = r[0].split('&')[0]
            search = search.replace('wd=', '').replace('+', ' ')
            if search:
                print '\n[*] -- Found Baidu -- '
                print '[+] %s - Search For: %s' % (date, search)
        if 'google' in url.lower():
            r = re.findall(r'q=.*\&', url)
            search = r[0].split('&')[0]
            search = search.replace('q=', '').replace('+', ' ')
            if search:
                print '\n[*] -- Found Google -- '
                print '[+] %s - Search For: %s' % (date, search)
    conn.close()

def main():
    usage = "%prog -p <firefox profile path>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-p', dest='pathName', type='string',\
                    help='specify firefox profile path')
    (options, args) = parser.parse_args()

    pathName = options.pathName
    pathName = "C:\Users\dcs\AppData\Roaming\Mozilla\Firefox\Profiles\kqbdnihc.default\places.sqlite"
    if pathName == None:
        print parser.print_help()
        exit(0)
    elif os.path.isdir(pathName) == False:
        print '\n[!] Path is not Exist: ' + pathName
        exit(0)
    downloadDB = os.path.join(pathName, 'downloads.sqlite')
    if os.path.isfile(downloadDB):
        printDownloads(downloadDB)
    else:
        print '\n[!] DownloadsDb does not exist: '+downloadDB
    placesDB = os.path.join(pathName, 'places.sqlite')
    if os.path.isfile(placesDB):
        printHistory(placesDB)
        printBaidu(placesDB)
    else:
        print '[!] PlacesDb does not exist: '+placesDB

if __name__ == "__main__":
    main()
#    printDownloads("C:\Users\dcs\AppData\Roaming\Mozilla\Firefox\Profiles\kqbdnihc.default\places.sqlite")


    '''
    SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说
    没有独立的维护进程，所有的维护都来自于程序本身。
    在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
    连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
    数据库文件，而是直接打开该数据库文件。
    连接对象可以是硬盘上面的数据库文件，也可以是建立在内存中的，在内存中的数据库
    执行完任何操作后，都不需要提交事务的(commit)

    创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
    创建在内存上面： conn = sqlite3.connect('"memory:')

    下面我们一硬盘上面创建数据库文件为例来具体说明：
    conn = sqlite3.connect('c:\\test\\hongten.db')
    其中conn对象是数据库链接对象，而对于数据库链接对象来说，具有以下操作：

        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

    cu = conn.cursor()
    这样我们就创建了一个游标对象：cu
    在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
    对于游标对象cu，具有以下具体操作：

        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动

    '''
