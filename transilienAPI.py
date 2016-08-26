#!/usr/bin/python3

""" this module retrieves times of the trains from Transilien API """

# TODO Finish implementation

CHARS = 'Chars'
PONTOISE = 'Pontoise'
SARTOUVILLE = 'Sartrouville'
PSL = 'Paris Saint-Lazare'

urls = {
    "chars"        : ('nomGare=CHARS'),
    "pontoise"     : ('nomGare=PONTOISE'),
    "p-chars"      : ('nomGare=PONTOISE&destination=CHARS'),
    "sartrouville" : ('nomGare=SARTROUVILLE'),
    "s-cergypref"  : ('nomGare=SARTROUVILLE&destination=CERGY+PREFECTURE'),
    "psl"          : ('nomGare=GARE+DE+PARIS+SAINT-LAZARE'),
    "psl-nu"       : ('nomGare=GARE+DE+PARIS+SAINT-LAZARE&destination=NANTERRE+UNIVERSITE'),
    "psl-pontoise" : ('nomGare=GARE+DE+PARIS+SAINT-LAZARE&destination=PONTOISE'),
}