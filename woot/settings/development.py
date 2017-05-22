
### django
### local
from woot.settings.common import *

### util
from os import environ


##################################################################################################
########################################## DJANGO CONFIGURATION CHANGES
##################################################################################################
### These changes are made to test in a development environment

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
SITE = 'http://localhost:8000'
SITE_TYPE = 'DEVELOPMENT'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
########## END DEBUG CONFIGURATION


########## CACHE CONFIGURATION
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	}
}
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = 'x08ig!20zeo%q46l6dnc8eqzb5g+h&(t4o18e#!yex&g&7sn=n'
########## END SECRET CONFIGURATION


########## EMAIL DEBUG CONFIGURATION
# Show emails in the console during developement.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

########## EMAIL SERVER CONFIGURATION
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'arkticvoice.noreply@gmail.com'
EMAIL_HOST_PASSWORD = 'uqnhs77f'
SERVER_EMAIL = EMAIL_HOST_USER

########## END EMAIL SERVER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'db/db.sqlite3',
	}
}
########## END DATABASE CONFIGURATION

##################################################################################################
########################################## END DJANGO CONFIGURATION CHANGES
##################################################################################################
