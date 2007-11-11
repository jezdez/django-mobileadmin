import os
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join
from middleware import get_thread_var

TEMPLATE_DIR =  os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

def load_template_source(template_name, template_dirs=None):
    """
    Custom template loader which loads the requested template from the
    mobileadmin template directory if the iPhone/iPod touch user agent string
    has been detected by the ``MobileAdminMiddleware`` while proccessing the
    request.
    """
    tried = []
    filepath = safe_join(TEMPLATE_DIR, template_name)
    if get_thread_var('use_mobile_templates'):
        try:
            return (open(filepath).read().decode(settings.FILE_CHARSET), "mobile:%s" % filepath)
        except IOError:
            tried.append(filepath)
    if tried:
        error_msg = "Tried %s" % tried
    else:
        error_msg = "Please make sure the template loader is the first item in settings.TEMPLATE_LOADERS"
    raise TemplateDoesNotExist, error_msg
load_template_source.is_usable = True
