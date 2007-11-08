import os, re
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.utils.cache import patch_vary_headers

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()

safari_regex = re.compile(r'AppleWebKit/.*Mobile/')

def normalize_slashes(path):
    """
    Removes leading, trailing and multiple slashes from a given path
    
    >>> path = "/asd/ad/"
    >>> normalize_slashes(path)
    'asd/ad'
    >>> path = "/asdasd///asd///asd/aa/"
    >>> normalize_slashes(path)
    'asdasd/asd/asd/aa'
    """
    return "/".join([x for x in path.strip().split("/") if x])

def get_thread_var(var_name):
    """
    Loads variable from the local thread
    """
    return getattr(_thread_locals, var_name, None)

def set_thread_var(var_name, value):
    """
    Sets variable in the local thread   
    """
    setattr(_thread_locals, var_name, value)

class MobileAdminMiddleware:
    """
    Checks for the iPhone/iPod touch user agent string if the admin interface
    is requested. Sets a thread var which is later used in a custom template
    loader to decide which template to load.
    
    Adds the User-Agent field to the Vary header to circumvent false caching.
    """
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'django.contrib.admin' in settings.INSTALLED_APPS:
            try:
                admin_url = normalize_slashes(reverse('django.contrib.admin.views.main.index'))
            except NoReverseMatch:
                admin_url = None
            if admin_url is not None and \
                safari_regex.search(user_agent) is not None and \
                    normalize_slashes(request.path).startswith(admin_url):
                set_thread_var('use_mobile_templates', True)
            else:
                set_thread_var('use_mobile_templates', False)
            return None

    def process_response(self, request, response):
        if get_thread_var('use_mobile_templates') is not None:
            patch_vary_headers(response, ('User-Agent',))
        return response
