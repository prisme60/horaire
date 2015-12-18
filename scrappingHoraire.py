#!/usr/bin/python3

""" this module retrieves times of the trains from website (RATP, Transilien) """

# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html
import urllib.request
import gzip

def selecteur_transilien(root:object):
    # Use cssselect to select elements by their css code
    horaires = root.cssselect("#map_b table.recherche-horaires-resultats tbody tr")      # returns 7 elements (1 header and 6 data)
    fields = {}

    if len(horaires)>0:
        fields = {"code"       :"td.train span.code",
                  "heure"      :"td span.hour",
                  "destination":"td.train + td + td",
                  "voie"       :"td span.pathway"}

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
    horaires, fields = horaires_fct(pathInfo)

    extractions = []
    for horaire in horaires:
        dict_horaire = {}
        for k, v in fields.items():
            texte = ""
            for resField in horaire.cssselect(v):
                for itText in resField.itertext():
                    texte += itText.strip()
            dict_horaire[k] = texte
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
  req = urllib.request.Request('http://www.transilien.com/horaires/prochains-departs')
  req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
  req.add_header('Accept-Encoding', 'gzip')
  #resource = urllib.request.urlopen(req,b'nomGare=PONTOISE')
  resource = urllib.request.urlopen(req, data)
  #try:
  r = gzip.decompress(resource.read())
  #except OSError:
  #  pass
  content = r.decode('utf-8')
  #print(content)
  root = lxml.html.document_fromstring(content)
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
#                   print itText.strip() 
            item.append(texte)
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


# POST http://www.transilien.com/horaires/prochains-departs
# Content-Type: application/x-www-form-urlencoded
# nomGare=CHARS
#  -- response --
# 200 OK
# Server:  Apache-Coyote/1.1
# X-Powered-By:  Servlet 2.5; JBoss-5.0/JBossWeb-2.1
# Content-Type:  text/html;charset=UTF-8
# Content-Language:  fr-FR
# Content-Encoding:  gzip
# Vary:  Accept-Encoding
# X-Varnish:  131270449, 150663663
# Transfer-Encoding:  chunked
# Date:  Wed, 02 Dec 2015 16:20:54 GMT
# Age:  0
# Connection:  keep-alive
# Via:  1.1 varnish, 1.1 bou2-ncdn-middle-http00, 1.1 bou2-ncdn-edge-http00



urls = {
"chars"        : (horaires_transilien,b'nomGare=CHARS'),
"pontoise"     : (horaires_transilien,b'nomGare=PONTOISE'),
"p-chars"      : (horaires_transilien,b'nomGare=PONTOISE&destination=CHARS'),
"sartrouville" : (horaires_transilien,b'nomGare=SARTROUVILLE'),
"s-cergypref"  : (horaires_transilien,b'nomGare=SARTROUVILLE&destination=CERGY+PREFECTURE'),
"psl"          : (horaires_transilien,b'nomGare=GARE+DE+PARIS+SAINT-LAZARE'),
"psl-nu"       : (horaires_transilien,b'nomGare=GARE+DE+PARIS+SAINT-LAZARE&destination=NANTERRE+UNIVERSITE'),
"psl-pontoise" : (horaires_transilien,b'nomGare=GARE+DE+PARIS+SAINT-LAZARE&destination=PONTOISE'),
"auber"        : (horaires_ratp      ,'http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/RA/Auber/A'),
"lepecq"       : (horaires_ratp      ,'http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/RA/Le+Vesinet+le+Pecq/R')
}

if __name__ == '__main__':
    for code, (selecteurSite, url) in urls.items():
        print("--------------" + code + "--------------")
        print(horaires(code))

