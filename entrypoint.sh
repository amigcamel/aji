python manage.py collectstatic --noinput
uwsgi --socket shared/aji.sock --wsgi-file aji/wsgi.py --chmod-socket=666
