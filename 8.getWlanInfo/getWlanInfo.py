# -*- coding:utf-8 -*-
__author__ = 'dscdtc'

import _winreg
import sys
#print sys.getdefaultencoding() #ascii
reload(sys)
sys.setdefaultencoding('GB2312')

def val2addr(val):
    addr = ''
    for ch in val:
        addr += '%02x ' % ord(ch)   #format output;ord(): ascii<->dec
    addr = addr.strip(" ").replace(" ", ":")[0:17]
    return addr

def printNets():
    net = "SOFTWARE\Microsoft\Windows NT" + \
        "\CurrentVersion\NetworkList\Signatures\Unmanaged"
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, net)
    print '[*] Networks You have joined:'
    for i in range(100):
        try:
            guid = _winreg.EnumKey(key, i)
            netKey = _winreg.OpenKey(key, str(guid))
            (n, addr, t) = _winreg.EnumValue(netKey, 5)
            (n, name, t) = _winreg.EnumValue(netKey, 4)
            #name = unicode(name,'GBK').encode('UTF-8')
            if addr:
                macAddr = val2addr(addr)
            else:
                macAddr = ''
            netName = str(name)
            print '[+] %s: %s' % (netName, macAddr)
            _winreg.CloseKey(netKey)
        except:
			print ("\n  There are %d records.") % i
			break

def main():
    printNets()
    
if __name__ == "__main__":
    main()