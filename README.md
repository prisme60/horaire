Horaire
======================

Ensemble de scripts python pour récupérer les horaires de trains (transilien ou grande ligne) en France, avec possibilité de les envoyer par SMS (uniquement free mobile)

wsgi.py : point d'entrée du wsgi

enable_wlan.py : active/désactive le Wifi à la maison

form.html : fichier html qui contient le formulaire, afin de préparer le texte à envoyer par SMS

scrappingHoraire.py : librairie pour extraire les données des fichiers html du site du transilien ou ratp

jsonHoraire.py : récupération du JSON du site gare-scnf.com et extraction des données (grandes lignes arrivées et départs)

sendHoraireSMS.py : extration des horaires, suivi de son formatage et puis envoie par SMS (s'intègre facilement dans une tâche CRON)

sendSMS.py : envoie de SMS via l'API de free mobile

