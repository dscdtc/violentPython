__author__ = 'dscdtc'

import os
import sys
import _winreg

reload(sys)
sys.setdefaultencoding('GB2312')

def returnDir(drive):
    dirs = [':\\Recycler\\',\
            ':\\Recycled\\',\
            ':\\$Recycle.Bin\\']

    for recycleDir in dirs:
        recycleDir = drive + recycleDir
        if os.path.isdir(recycleDir):
            return recycleDir
    return None

def sid2user(sid):
    try:
        net = 'SOFTWARE\Microsoft\Windows NT' + '\CurrentVersion\ProfileList\%s' % sid
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, net)
        (value, type) = _winreg.QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except:
        return sid

def findRecycled(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)
        print '[*] In User: ' + str(user)
        for file in files:
            print '[+] Found File: ' + str(file)

def main():
    for drive in list('CDEFGHIJKLMNOPQRSTUVWXYZ'):
        recycleDir = returnDir(drive)
        if recycleDir:
            print ("\n    %s:\>There are:") % drive
            findRecycled(recycleDir)

if __name__ == "__main__":
    __author__ = 'dscdtc'
    main()
