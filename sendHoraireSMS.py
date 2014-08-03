#!/usr/bin/python3

import sys
import sendSMS
import scrappingHoraire

def horaireStr(tabtab):
    result = ""
    for tab in tabtab:
        result += " ".join(tab)
        result += "\r"
    print(result)
    return result

def sendHoraire(pathInfo):
    if pathInfo in scrappingHoraire.getUrls():
        sendSMS.writeMsg(horaireStr(scrappingHoraire.horaires(pathInfo)))
    else:
        sendSMS.writeMsg('sendHoraire.py : Cant find pathInfo=' + pathInfo)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sendHoraire(sys.argv[1])
    elif len(sys.argv) > 2:
        sendSMS.writeMsg('sendHoraire.py : Too much Args')
    else:
        sendSMS.writeMsg('sendHoraire.py : No args')

