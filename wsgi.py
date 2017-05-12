#!/usr/bin/python3

import enable_wlan
import scrappingHoraire
import jsonHoraire
import sendSMS
import sendMsgToDisplay
import urllib.parse
import transilienAPI


def horairesHTML(pathInfo, source_fct):
    extractions = source_fct(pathInfo)
    htmlStr = "<table>"
    for extraction in extractions:
        htmlStr += "<tr>"
        for field in extraction:
            htmlStr += "<td>" + str(field) + "</td>"
        htmlStr += "</tr>"
    htmlStr += "</table>"
    return [htmlStr.encode("utf-8")]

def displayEnv(env):
    response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(env.items())]
    return ['<p>\n'.join(response_body).encode("utf-8")]

def listeActionHTML():
    htmlStr = ""
    for code, (action, param) in sorted(urls_action.items()):
        htmlStr += '<a href="' + code + '">' + code + "</a><p/>"
    return htmlStr.encode("utf-8")

def exec_action(key, queryString, body):
    (action, param) = urls_action[key]
    return [action(key, param, queryString, body).encode("utf-8")]

def wlanSet(key, enable, queryString, body):
    enable_wlan.wlan_interface(enable)
    return key + ': wlan_interface(' + str(enable) + ') executed!'

def wlanState(key, notUsed, queryString, body):
    state = enable_wlan.wlan_interface_state()
    return key + ': ' + ('ON' if state else 'OFF')

def alarmSet(key, notUsed, queryString, body):
    dict = urllib.parse.parse_qs(body.decode('utf-8'))
    #return ', '.join("{!s}={!r}".format(key,val) for (key,val) in dict.items()).encode('utf-8')
    #return dict[b'msg'][0]
    sendMsgToDisplay.sendMsg(dict['msg'][0], 'wsgi')
    return "Alarm displayed"

def msgSet(key, notUsed, queryString, body):
    """no treatment on the body (we send exactly the body like we received it)"""
    dict = urllib.parse.parse_qs(body.decode('utf-8'))
    #sendSMS.writeRawMsg(body)
    user = dict['user'][0]
    print(dict)
    sendSMS.writeMsgUser(dict['msg'][0], user)
    return "Message sent to " + user

urls_action = {
    "wlanON" : (wlanSet, True),
    "wlanOFF" : (wlanSet, False),
    "wlan" : (wlanState, None),
    "writeAlarm" : (alarmSet, None),
    "writeMsg" : (msgSet, None)
}

def listeGaresHTML():
    list_code_gare =[]
    htmlStr = ""
    for code in scrappingHoraire.getUrls().keys():
        list_code_gare.append(code)
    for code in jsonHoraire.getUrls().keys():
        list_code_gare.append(code)
    for code in transilienAPI.getUrls().keys():
        list_code_gare.append(code)
    for code in sorted(list_code_gare):
        htmlStr += '<a href="' + code + '">' + code + "</a><p/>"
    return htmlStr.encode("utf-8")

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    body = ''  # b'' for consistency on Python 3.0
    try:
        length_str = env.get('CONTENT_LENGTH', '0')
        length = int(length_str)
    except ValueError:
        length = 0
    if length != 0:
        body = env['wsgi.input'].read(length)
#    return body
#    return displayEnv(env)
    pathInfo = env["PATH_INFO"]
    if pathInfo in urls_action:
        return exec_action(pathInfo, env["QUERY_STRING"], body)
    elif pathInfo in scrappingHoraire.getUrls():
        return horairesHTML(pathInfo, scrappingHoraire.horaires)
    elif pathInfo in jsonHoraire.getUrls():
        return horairesHTML(pathInfo, jsonHoraire.horaires)
    elif pathInfo in transilienAPI.getUrls():
        return horairesHTML(pathInfo, transilienAPI.horaires)
    else:
        return [listeGaresHTML()+listeActionHTML()]

if __name__ == '__main__':
    for code in scrappingHoraire.getUrls().keys():
        print(horairesHTML(code, scrappingHoraire.horaires))
    for code in jsonHoraire.getUrls().keys():
        print(horairesHTML(code, jsonHoraire.horaires))
    for code in transilienAPI.getUrls().keys():
        print(horairesHTML(code, transilienAPI.horaires))
    print([listeGaresHTML()+listeActionHTML()])
    for (key, (action, param)) in urls_action.items():
        print(action(key, param, "", 'msg=Coucou%20a%20tous'.encode()))


