#!/usr/bin/python3

""" this module retrieves times of the trains from website (RATP, Transilien) """

# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html
import urllib.request
import gzip
import re
import time

def selecteur_transilien(root:object):
    # Use cssselect to select elements by their css code
    #test = root.cssselect("#map_b")
    #print(lxml.etree.tostring(test[0]))

    horaires = root.cssselect("li.resultat_gare")      # returns 7 elements (1 header and 6 data)
    fields = {}

    # TODO à tester

    if len(horaires)>0:
        fields = {"code"       :"rain_mission",
                  "heure"      :".heure_train",
                  "destination":".garearrivee",
                  "voie"       :"voie.bock"}

    return horaires, fields

def selecteur_RATP(root:object):
    # Use cssselect to select elements by their css code
    horaires = root.cssselect(".rer table tbody tr")      # returns n elements
    fields = {}
    if len(horaires)>=1:
        fields = {"code"       :".name",
                  "destination":".terminus",
                  "situation"  :".passing_time"}
    return horaires, fields

def horaires_dict(pathInfo:str):
    """ return extracted times according given pathInfo with dictionary format """
    (horaires_fct, url) = urls[pathInfo]
    horaires, fields = horaires_fct(url)

    extractions = []
    for horaire in horaires:
        dict_horaire = {}
        for k, v in fields.items():
            texte = ""
            for resField in horaire.cssselect(v):
                for itText in resField.itertext():
                    texte += itText.strip()
            textOneSpace = re.sub('\s+',' ',texte)
            dict_horaire[k] = textOneSpace
        extractions.append(dict_horaire)
    return extractions
    
def horaires_ratp(url):
    """ return extracted times according given pathInfo with list format (ready to display) """
    #print help(lxml.html.parse)
    #print("url=" + url)    
    # To load directly from a url, use
    root = lxml.html.parse(url).getroot()
    
    # Whenever you have an lxml element, you can convert it back to a string like so:
    #print lxml.etree.tostring(root)

    return selecteur_RATP(root)

def horaires_transilien(data):
  url = 'http://www.transilien.mobi/train/result?' + data
  root = lxml.html.parse(url).getroot()
  return selecteur_transilien(root)


def horaires(pathInfo:str):
    """ return extracted times according given pathInfo with list format (ready to display) """
    (horaires_fct, data) = urls[pathInfo]
    horaires, fields = horaires_fct(data)

    extractions = []
    for horaire in horaires:
        item = []
        for k, v in fields.items():
            texte = ""
            for resField in horaire.cssselect(v):
                for itText in resField.itertext():
                    texte += itText.strip()
            textOneSpace = re.sub('\s+',' ',texte)
            item.append(textOneSpace)
        extractions.append(item)
    
    #print extractions
    
    # extracting text from a single element 
    #linimble = root.cssselect("ul #nimble")[0]
    #help(linimble)                       # prints the documentation for the object
    #print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
    #print linimble.text                  # just the text between the tag
    #print linimble.tail                  # the trailing text
    #print list(linimble)                 # prints the <b> object

    return extractions

def getUrls():
    return urls


CHARS = 'CHR'
PONTOISE = 'PSE'
PSL = 'PSL'
SARTROUVILLE = 'SVL'
CERGYPREF = 'CYP'
NANTERRE_UNIVERSITE = 'NUN'

urls = {
"chars"        : (horaires_transilien, 'idOrigin=' + CHARS),
"pontoise"     : (horaires_transilien, 'idOrigin=' + PONTOISE),
"p-chars"      : (horaires_transilien, 'idOrigin=' + PONTOISE),
"sartrouville" : (horaires_transilien, 'idOrigin=' + SARTROUVILLE),
"s-cergypref"  : (horaires_transilien, 'idOrigin=' + SARTROUVILLE + '&idDest=' + CERGYPREF),
"psl"          : (horaires_transilien, 'idOrigin=' + PSL),
"psl-nu"       : (horaires_transilien, 'idOrigin=' + PSL + '&idDest=' + NANTERRE_UNIVERSITE),
"psl-pontoise" : (horaires_transilien, 'idOrigin=' + PSL + '&idDest=' + PONTOISE),
"auber"        : (horaires_ratp      ,'http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/RA/Auber/A'),
"lepecq"       : (horaires_ratp      ,'http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/RA/Le+Vesinet+le+Pecq/R')
}

if __name__ == '__main__':
    for code, (selecteurSite, url) in urls.items():
        print("--------------" + code + "--------------")
        time.sleep(1)
        print(horaires(code))

