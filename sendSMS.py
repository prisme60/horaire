#!/usr/bin/python3

import sys
import urllib
from urllib import parse
from urllib import request
from accounts import Accounts

def writeRawMsgUser(rawMsg, user):
    values = Accounts.accounts[user]
    #print("rawMsg " + repr(rawMsg))
    rawMsgFiltered = rawMsg.decode().replace('%0A%0D','%0A').replace('%0D','%0A') #because \n is not managed by free mobile, we need to replace it by \r
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(Accounts.the_url + '?' + data + '&' + rawMsgFiltered)
    handle = urllib.request.urlopen(req)
    the_page = handle.read()

def writeRawMsg(rawMsg):
    writeRawMsgUser(rawMsg, 'cf')

def writeMsgUser(msg, user):
    values =  Accounts.accounts[user]   
    values['msg'] = msg.encode('utf-8')
    data = urllib.parse.urlencode(values)
    
    #req = urllib.request.Request(the_url, data)
    req = urllib.request.Request(b(Accounts.the_url + '?' + data))
    handle = urllib.request.urlopen(req)
    the_page = handle.read()

def writeMsg(msg):
    writeMsgUser(msg, 'cf')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        writeMsg(" ".join(sys.argv[1:]))
    else:
        writeMsg('Hello from Raspberry pi! (message vide)')
