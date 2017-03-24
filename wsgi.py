# django
from django.core.wsgi import get_wsgi_application

# util
import os

# set environ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woot.settings.development')
application = get_wsgi_application()
