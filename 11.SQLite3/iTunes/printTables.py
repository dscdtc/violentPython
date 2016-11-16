import os
import sqlite3
def printTables(iphoneDB):
    try:
        conn = sqlite.connect(iphoneDB)
        c = conn.cursor()
        c.execute('SELECT tbl_name FROM sqlite_master \
                WHERE type==\"table\";')
        print '\n[*] Database: '+iphoneDB
        for row in c:
            print "[-] Table: "+str(row)
        except:
            pass
        finally:
            conn.close()

dirList = os.listdir(os.getcwd())
for fileName in dirList:
    printTables(fileName)