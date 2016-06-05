#!/usr/bin/python3

import urllib.request
import json

""" this module retrieves times of the trains from website (SNCF) """


def selecteur_gare_sncf(myurl:str):
    #body = {'ids': [12, 14, 50]}
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    #jsondata = json.dumps(body)
    #jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    #req.add_header('Content-Length', len(jsondataasbytes))
    #print(jsondataasbytes)
    #response = urllib.request.urlopen(req, jsondataasbytes)
    resource = urllib.request.urlopen(req)
    charset = print(resource.headers.get_content_charset())
    if charset is None:
        charset = 'utf-8'
    content = resource.read().decode(charset)
    print(content)
    dic = json.loads(content, encoding=charset)
    print(dic['trains'])

    fields = ['heure', 'origdest', 'voie', 'type', 'num', 'voie_attr', 'retard', 'infos']

    return dic['trains'], fields


def horaires_dict(path_info):
    """ return extracted times according given pathInfo with dictionary format """
    (selecteur, url) = urls[path_info]
    dic, fields = selecteur(url)
    extractions = []
    #replace numerated dictionary by an array
    for subdic in dic:
        extractions.append(subdic)
    return extractions


def horaires(path_info):
    """ return extracted times according given pathInfo with dictionary format """
    (selecteur, url) = urls[path_info]
    dic, fields = selecteur(url)
    extractions = []
    for subdic in dic:
        extraction = []
        for field in fields:
            extraction.append(replace_field(field, subdic[field]))
        extractions.append(extraction)
    return extractions


def replace_field(field, value):
    """ if Retard field is not empty, replace content by retard: """
    if field == 'retard':
        if value is None or value == '':
            return ''
        else:
            return 'retard :'
    else:
        return value


def getUrls():
    return urls

urls = {
    "psl_d": (selecteur_gare_sncf, 'http://www.gares-sncf.com/fr/train-times/PSL/departure'),
    "psl_a": (selecteur_gare_sncf, 'http://www.gares-sncf.com/fr/train-times/PSL/arrival')
}

if __name__ == '__main__':
    for code, (selecteurSite, url) in urls.items():
        print(horaires(code))

