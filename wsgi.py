#!/usr/bin/python

import enable_wlan
import scrappingHoraire
import sendSMS

def horairesHTML(pathInfo):
    extractions = scrappingHoraire.horaires(pathInfo)
    htmlStr = "<table>"
    for extraction in extractions:
        htmlStr += "<tr>"
	for field in extraction:
	     htmlStr += "<td>" + field + "</td>"
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
    (action,param) = urls_action[key]
    return [action(key, param, queryString, body)]

def wlanSet(key, enable, queryString, body):
    enable_wlan.wlan_interface(enable)
    return key + ': wlan_interface(' + str(enable) + ') executed!'

def wlanState(key, notUsed, queryString, body):
    state = enable_wlan.wlan_interface_state()
    return key + ': ' + ('ON' if state else 'OFF')

def msgSet(key, notUsed, queryString, body):
    sendSMS.writeRawMsg(body)
    return "Message sent"

urls_action = {
"wlanON" : (wlanSet, True),
"wlanOFF" : (wlanSet, False),
"wlan" : (wlanState,None),
"writeMsg" : (msgSet, None)
}

def listeGaresHTML():
    htmlStr = ""
    for code, (selecteur, url) in sorted(scrappingHoraire.getUrls().items()):
        htmlStr += '<a href="' + code + '">' + code + "</a><p/>"
    return htmlStr.encode("utf-8")

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    body= '' # b'' for consistency on Python 3.0
    try:
        length_str = env.get('CONTENT_LENGTH',"0") 
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
	return horairesHTML(pathInfo)
    else:
        return [listeGaresHTML()+listeActionHTML()]

if __name__ == '__main__':
    for code, (selecteurSite,url) in scrappingHoraire.getUrls().items():
	print horairesHTML(code)
    print [listeGaresHTML()+listeActionHTML()]
    for (key,(action,param)) in urls_action.items():
        print action(key,param,"","msg=Coucou%20a%20tous")


