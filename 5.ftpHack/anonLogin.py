import ftplib

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] %s FTP Anonymous Logon Succeed.' % hostname
        ftp.quit()
        return True
    except Exception, e:
        print '[-] FTP Anonymous Logon Failed.'
        return False

def main():
    for x in range(200):
        host = '143.166.83.%d' % x
        anonLogin(host)
    
if __name__ == '__main__':
    main()

