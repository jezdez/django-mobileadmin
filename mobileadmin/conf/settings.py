import os
from django.conf import settings

MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'media')
MEDIA_PREFIX = getattr(settings, 'MOBILEADMIN_MEDIA_PREFIX', '/mobileadmin_media/')
MEDIA_REGEX = r'^%s(?P<path>.*)$' % MEDIA_PREFIX.lstrip('/')

COOKIE_AGE = getattr(settings, 'MOBILEADMIN_COOKIE_AGE', settings.SESSION_COOKIE_AGE)

# A string like ".lawrence.com", or None for standard domain cookie.
COOKIE_DOMAIN = getattr(settings, 'MOBILEADMIN_COOKIE_DOMAIN', settings.SESSION_COOKIE_DOMAIN)
