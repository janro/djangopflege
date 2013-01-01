manage.py dumpdata > data.json
manage.py reset cadmin
manage.py syncdb
manage.py loaddata data.json