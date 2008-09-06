"""
Middleware sets a flag, when a mobile device is requesting the site.

This is used later on to load special mobile-admin templates.

"""

import os
import re
import time
from django.conf import settings
from django.utils.http import cookie_date
from django.utils.cache import patch_vary_headers
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import Template, Context
from django.utils.encoding import force_unicode
from mobileadmin.conf.settings import COOKIE_AGE, COOKIE_DOMAIN

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()

safari = re.compile(r'AppleWebKit/.*Mobile/')
blackbarry = re.compile(r'^BlackBerry')
opera_mini = re.compile(r'[Oo]pera [Mm]ini')

TOGGLE_TEMPLATE = """\
<script type="text/javascript" charset="utf-8">
    $('toggle').addEventListener('click', function() {
        toggle('on', {{ age }}, '{{ admin_url }}', {{ secure|yesno:"true,false" }});
    }, false);
</script>
"""

def is_valid_user_agent(user_agent):
    """
    Checks if the given user agent string matches one of the valid user agents.
    """
    valid_user_agents = (safari, blackbarry, opera_mini)
    for regex in valid_user_agents:
        if regex.search(user_agent) is not None:
            return True
    return False

def normalize_slashes(path):
    """
    Removes leading, trailing and multiple slashes from a given path.

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
    Loads variable from the local thread.
    """
    return getattr(_thread_locals, var_name, None)

def set_thread_var(var_name, value):
    """
    Sets variable in the local thread.
    """
    setattr(_thread_locals, var_name, value)

class MobileAdminMiddleware:
    """
    Checks for the some mobile device user agent strings, when the
    admin interface is requested. Sets a thread var which is later used
    in a custom template loader to decide which template to load.

    Adds the User-Agent field to the Vary header to circumvent false
    caching.

    These browsers are supported:

        * Safari (iPhone / iPod touch)
        * BlackBerry's internal browser
        * `Opera mini`_

    .. _Opera mini: http://www.operamini.com/demo/
    """
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        cookie = request.COOKIES.get('mobileadmin')
        toggle = request.GET.get('mobileadmin')
        use_mobileadmin = True
        if 'django.contrib.admin' in settings.INSTALLED_APPS:
            try:
                admin_url = normalize_slashes(
                    reverse('django.contrib.admin.views.main.index'))
            except NoReverseMatch:
                admin_url = None
            if use_mobileadmin and admin_url is not None and \
                is_valid_user_agent(user_agent) and \
                normalize_slashes(request.path).startswith(admin_url):
                set_thread_var('use_mobile_templates', True)
            else:
                set_thread_var('use_mobile_templates', False)
            return None

    def process_response(self, request, response):
        try:
            admin_url = normalize_slashes(
                reverse('django.contrib.admin.views.main.index'))
        except NoReverseMatch:
            admin_url = None
        if admin_url is None or \
            'text/html' not in response['Content-Type'] or \
            request.is_ajax() or \
            response.status_code != 200:
            return response
        content = Template(TOGGLE_TEMPLATE).render(Context({
            'age': COOKIE_AGE,
            'admin_url': admin_url,
            'secure': request.is_secure(),
            'path': request.get_full_path(),
        }))
        old_content = response.content
        response.content = force_unicode(old_content).replace('</body>', content)
        return response
