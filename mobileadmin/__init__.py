import os

# If you want to serve the mobileadmin media files with Django or any other
# Python-based product, feel free to use something like this in your script:
# from mobilemedia import MOBILEADMIN_MEDIA_PATH
# with that you always get the most current version of the media files
MOBILEADMIN_MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')

VERSION = (0, 2, ".1")
