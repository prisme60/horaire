#!/usr/bin/python

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


def horaires(url,selecteur):
    #print help(lxml.html.parse)
    
    # To load directly from a url, use
    root = lxml.html.parse(url).getroot()

    # Whenever you have an lxml element, you can convert it back to a string like so:
    #print lxml.etree.tostring(root)

    horaires, fields = selecteur(root)

    extractions = []
    for horaire in horaires:
#        extractions.append([horaire.cssselect(v)[0].text.strip() for k,v in fields.items()])
        item = [];
        for k,v in fields.items():
            texte = ""
            for resField in horaire.cssselect(v):
                for itText in resField.itertext():
                    texte += itText.strip()
                    print itText.strip() 
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

def horairesHTML(url, selecteur):
    extractions =  horaires(url, selecteur)
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
    return ['\n'.join(response_body).encode("utf-8")]


urls = {
"pontoise"     : (selecteurTransilien,'http://www.transilien.com/gare/PONTOISE-8727613'),
"p"            : (selecteurTransilien,'http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=PSE&destination=&ligne=J&nomGare=PONTOISE&x=46&y=11'),
"sartrouville" : (selecteurTransilien,'http://www.transilien.com/gare/SARTROUVILLE-8738641'),
"s"            : (selecteurTransilien,'http://www.transilien.com/gare/pagegare/filterListeTrains?codeTR3A=SVL&destination=CERGY+PREFECTURE&ligne=&nomGare=SARTROUVILLE&x=38&y=11'),
"psl_d"        : (selecteurGareEnMvt ,'http://www.gares-en-mouvement.com/fr/frpsl/horaires-temps-reel/dep/'),
"psl_a"        : (selecteurGareEnMvt ,'http://www.gares-en-mouvement.com/fr/frpsl/horaires-temps-reel/arr/')
}

def listeGaresHTML():
    htmlStr = ""
    for code, (selecteur, url) in sorted(urls.items()):
        htmlStr += '<a href="' + code + '">' + code + "</a><p/>"
    return [htmlStr.encode("utf-8")]

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    #return displayEnv(env)
    pathInfo = env["PATH_INFO"]
    if pathInfo in urls:
        (selecteurSite , url ) = urls[pathInfo]
	return horairesHTML(url, selecteurSite)
    else:
        return listeGaresHTML()

if __name__ == '__main__':
    for code, (selecteurSite,url) in urls.items():
	print horairesHTML(url, selecteurSite)



