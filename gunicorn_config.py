command = '/usr/local/bin/gunicorn'
pythonpath = '/home/pi/horaire/'
bind = 'unix:/tmp/gunicorn_wsgi.sock'
workers = 1
user = 'www-data'
