import os
from django.conf import settings

MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'media')
MEDIA_PREFIX = getattr(settings, 'MOBILEADMIN_MEDIA_PREFIX', '/mobileadmin_media/')
MEDIA_REGEX = r'^%s(?P<path>.*)$' % MEDIA_PREFIX.lstrip('/')
