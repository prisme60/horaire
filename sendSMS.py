#!/usr/bin/python

import sys
import urllib
import urllib2
from accounts import Accounts

def writeRawMsgUser(rawMsg, user):
    values = Accounts.accounts[user]
    rawMsgFiltered = rawMsg.replace('%0A%0D','%0A').replace('%0D','%0A') #because \n is not managed by free mobile, we need to replace it by \r
    data = urllib.urlencode(values)
    req = urllib2.Request(Accounts.the_url + '?' + data + '&' + rawMsg)
    handle = urllib2.urlopen(req)
    the_page = handle.read()

def writeRawMsg(rawMsg):
    writeRawMsgUser(rawMsg, 'cf')

def writeMsgUser(msg, user):
    values =  Accounts.accounts[user]   
    values['msg'] = msg.encode('utf-8')
    data = urllib.urlencode(values)
    
    #req = urllib2.Request(the_url, data)
    req = urllib2.Request(Accounts.the_url + '?' + data)
    handle = urllib2.urlopen(req)
    the_page = handle.read()

def writeMsg(msg):
    writeMsgUser(msg, 'cf')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        writeMsg(" ".join(sys.argv[1:]))
    else:
        writeMsg('Hello from Raspberry pi! (message vide)')
