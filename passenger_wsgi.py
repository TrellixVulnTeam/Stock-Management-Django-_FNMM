import sys, os

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/inventory/')

INTERP = os.path.expanduser("~/.virtualenvs/inventory_env/bin/python3")

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0,'$HOME/.virtualenvs/inventory_env/bin')
sys.path.insert(0,'$HOME/.virtualenvs/inventory_env/lib/python3.6/site-packages/django')
sys.path.insert(0,'$HOME/.virtualenvs/inventory_env/lib/python3.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
