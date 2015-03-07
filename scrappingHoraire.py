#!/usr/bin/python3

""" this module retrieves times of the trains from website (RATP, Transilien, SNCF) """

# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

def selecteurTransilien(root):
    # Use cssselect to select elements by their css code
    horaires = root.cssselect(".etat_trafic tr")      # returns 7 elements (1 header and 6 data)
    fields = {}

    if len(horaires)>=1:
        del horaires[0]

        fields = {"code"       :".nom",
                  "heure"      :".nom + td",
                  "destination":".nom + td + td",
                  "voie"       :".nom + td + td + td + td"}
    return horaires, fields

def selecteurGareEnMvt(root):
    # Use cssselect to select elements by their css code
    horaires = root.cssselect(".tab_horaires_tps_reel tbody tr")      # returns n elements
    fields = {}
    if len(horaires)>=1:
        fields = {"code"       :".tvs_td_numero",
                  "heure"      :".tvs_td_heure",
                  "destination":".tvs_td_originedestination",
                  "situation"  :".tvs_td_situation",
                  "voie"       :".tvs_td_voie"}
    return horaires, fields

def selecteurRATP(root):
    # Use cssselect to select elements by their css code
    horaires = root.cssselect(".rer table tbody tr")      # returns n elements
    fields = {}
    if len(horaires)>=1:
        fields = {"code"       :".name",
                  "destination":".terminus",
                  "situation"  :".passing_time"}
    return horaires, fields

def horaires_dict(pathInfo):
    """ return extracted times according given pathInfo with dictionary format """
    (selecteur, url) = urls[pathInfo]
    # To load directly from a url, use
    root = lxml.html.parse(url).getroot()

    horaires, fields = selecteur(root)

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

def horaires(pathInfo):
    """ return extracted times according given pathInfo with list format (ready to display) """
    (selecteur, url) = urls[pathInfo]

    #print help(lxml.html.parse)
    #print("url=" + url)    
    # To load directly from a url, use
    root = lxml.html.parse(url).getroot()

    # Whenever you have an lxml element, you can convert it back to a string like so:
    #print lxml.etree.tostring(root)

    horaires, fields = selecteur(root)

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

urls = {
"chars"        : (selecteurTransilien,'http://www.transilien.com/gare/CHARS-8738119'),
"pontoise"     : (selecteurTransilien,'http://www.transilien.com/gare/PONTOISE-8727613'),
"p"            : (selecteurTransilien,'http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=PSE&destination=&ligne=J&nomGare=PONTOISE&x=46&y=11'),
"sartrouville" : (selecteurTransilien,'http://www.transilien.com/gare/SARTROUVILLE-8738641'),
"s"            : (selecteurTransilien,'http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=SVL&destination=CERGY+PREFECTURE&ligne=&nomGare=SARTROUVILLE&x=38&y=11'),
"psl"          : (selecteurTransilien,'http://www.transilien.com/gare/GARE-DE-PARIS-SAINT-LAZARE-8738400'),
"psll"         : (selecteurTransilien,'http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=PSL&destination=&ligne=L&nomGare=GARE+DE+PARIS+SAINT-LAZARE&x=26&y=12'),
"pslj"         : (selecteurTransilien,'http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=PSL&destination=&ligne=J&nomGare=GARE+DE+PARIS+SAINT-LAZARE&x=29&y=6'),
"psl_d"        : (selecteurGareEnMvt ,'http://www.gares-en-mouvement.com/fr/frpsl/horaires-temps-reel/dep/'),
"psl_a"        : (selecteurGareEnMvt ,'http://www.gares-en-mouvement.com/fr/frpsl/horaires-temps-reel/arr/'),
"auber"        : (selecteurRATP      ,'http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/RA/Auber/A'),
"lepecq"       : (selecteurRATP      ,'http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/RA/Le+Vesinet+le+Pecq/R')
}

if __name__ == '__main__':
    for code, (selecteurSite, url) in urls.items():
        print(horaires(code))

