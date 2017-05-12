#!/usr/bin/python3

from TransilienAccount import TransilienAccount
from codeUIC import get_uic_from_name, get_name_from_uic
import lxml.etree
import lxml.html
import urllib


""" this module retrieves times of the trains from Transilien API """

BASE_URL = 'http://api.transilien.com'
URLDEPART = BASE_URL + '/gare/{}/depart'
URLDEPARTARRIVEE = URLDEPART + '/{}'


def get_url_depart_uic(uic_depart:int):
    doc = URLDEPART.format(uic_depart)
    return doc


def get_url_depart(depart: str):
    uic_depart = get_uic_from_name(depart)
    if uic_depart > 0:
        return get_url_depart_uic(uic_depart)
    return None


def get_url_depart_arrivee_uic(uic_depart: int, uic_arrivee: int):
    doc = URLDEPARTARRIVEE.format(uic_depart, uic_arrivee)
    return doc


def get_url_depart_arrivee(depart: str, arrivee: str):
    uic_depart = get_uic_from_name(depart)
    uic_arrivee = get_uic_from_name(arrivee)
    if uic_depart > 0 and uic_arrivee > 0:
        return get_url_depart_arrivee_uic(uic_depart, uic_arrivee)
    return None


def get_url(val):
    if type(val) is str:
        return get_url_depart(val)
    elif type(val) is tuple:
        if len(val) == 1:
            return get_url_depart(*val)
        elif len(val) == 2:
            return get_url_depart_arrivee(*val)
    return None


def get_url_from_key(pathInfo: str):
    return get_url(urls[pathInfo])


def horaires_dict(pathInfo: str):
    (login, password) = TransilienAccount.account

    manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, BASE_URL, login, password)
    auth = urllib.request.HTTPBasicAuthHandler(manager)
    opener = urllib.request.build_opener(auth)
    urllib.request.install_opener(opener)

    http_url = get_url_from_key(pathInfo)
    xml = urllib.request.urlopen(http_url).read()
    root = lxml.etree.XML(xml)
    trains = root.xpath('//passages/train')
    result = []
    for train in trains:
        uic_dest_str = train.xpath('term/text()')
        uic_dest_int = int(*uic_dest_str)
        dest = get_name_from_uic(uic_dest_int)
        result.append({
            'heure': train.xpath('date/text()')[0],
            'reel': train.xpath('date/@mode')[0],
            'num': train.xpath('num/text()')[0],
            'code': train.xpath('miss/text()')[0],
            'dest': dest,
        })
    return result


def horaires(pathInfo:str ):
    list = horaires_dict(pathInfo)
    return [dico.values() for dico in list]


def getUrls():
    return urls


CHARS = 'Chars'
PONTOISE = 'Pontoise'
SARTROUVILLE = 'Sartrouville'
PSL = 'Paris Saint-Lazare'
CERGYPREF = 'Cergy Préfecture'
NANTERREU = 'Nanterre Université'


urls = {
    "t_chars":        CHARS,
    "t_pontoise":     PONTOISE,
    "t_p-chars":      (PONTOISE, CHARS),
    "t_sartrouville": SARTROUVILLE,
    "t_s-cergypref":  (SARTROUVILLE, CERGYPREF),
    "t_psl":          PSL,
    "t_psl-nu":       (PSL, NANTERREU),
    "t_psl-pontoise": (PSL, PONTOISE),
}


if __name__ == '__main__':
    for (pathInfo, data) in urls.items():
        print(pathInfo + ' : ' + repr(horaires(pathInfo)))