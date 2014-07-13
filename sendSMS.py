#!/usr/bin/python

import sys
import urllib
import urllib2

the_url = 'https://smsapi.free-mobile.fr/sendmsg'

def writeRawMsg(rawMsg):
    values = {'user' : 'loginNumber',
              'pass' : 'PaSsWoRdStRiNg' }
    rawMsgFiltered = rawMsg.replace('%0A%0D','%0A').replace('%0D','%0A') #because \n is not managed by free mobile, we need to replace it by \r
    data = urllib.urlencode(values)
    req = urllib2.Request(the_url + '?' + data + '&' + rawMsg)
    handle = urllib2.urlopen(req)
    the_page = handle.read()


def writeMsg(msg):
    values = {'user' : 'loginNumber',
              'pass' : 'PaSsWoRdStRiNg',
              'msg' : msg.encode('utf-8') }

    data = urllib.urlencode(values)
    
    #req = urllib2.Request(the_url, data)
    req = urllib2.Request(the_url + '?' + data)
    handle = urllib2.urlopen(req)
    the_page = handle.read()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        writeMsg(" ".join(sys.argv[1:]))
    else:
        writeMsg('Hello from Raspberry pi! (message vide)')
