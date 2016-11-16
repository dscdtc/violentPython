__author__ = 'dscdtc'
import os
import optparse
# import sys
# reload(sys)
# sys.setdefaultencoding('GB2312')

try:
    from pyPdf import PdfFileReader
except:
    os.system('pip install -U pyPdf')
    from pyPdf import PdfFileReader

def printMeta(fileName):
    pdfFile = PdfFileReader(file(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print '[*] PDF MetaData For: ' +str(fileName)
    for metaItem in docInfo:
        print '[+] %s:%s' % (metaItem, docInfo[metaItem])

def main():
    usage = "usage: %prog -F <PDF file name>"
    parser = optparse.OptionParser(usage, version="%prog 1.0")
    parser.add_option('-F', dest='fileName', type='string',\
                    help='specify PDF file name')
    (options, args) = parser.parse_args()

    fileName = options.fileName
    if fileName == None:
        print '[-] You must specify a target host and port[s].'
        print parser.print_help()
        exit(0)
    else:
        printMeta(fileName)
        
if __name__ == '__main__':
    main()