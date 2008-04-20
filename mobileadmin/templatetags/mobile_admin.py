import os
import re
from django import template
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse, NoReverseMatch
from mobileadmin.conf import settings

register = template.Library()
absolute_url_re = re.compile(r'^(?:http(?:s)?:/)?/', re.IGNORECASE)

def mobileadmin_media_prefix(file_path=None):
    try:
        media_prefix = settings.MEDIA_PREFIX
        if file_path is not None:
            media_prefix = os.path.join(media_prefix, file_path)
        if not media_prefix.startswith('/'):
            return '/%s' % media_prefix
        return media_prefix

    except AttributeError:
        return ''
mobileadmin_media_prefix = register.simple_tag(mobileadmin_media_prefix)

def get_admin_root():
    try:
        admin_url = reverse('django.contrib.admin.views.main.index')
    except NoReverseMatch:
        admin_url = None
    return admin_url
get_admin_root = register.simple_tag(get_admin_root)

def truncate_dot(value, size):
    size = int(size)
    if len(value) > size and size > 3:
        return value[0:(size-3)] + '...'
    else:
        return value[0:size]
register.filter(truncate_dot)

def simple_unordered_list(value):
    def convert_old_style_list(list_):
        if not isinstance(list_, (tuple, list)) or len(list_) != 2:
            return list_, False
        first_item, second_item = list_
        if second_item == []:
            return [first_item], True
        old_style_list = True
        new_second_item = []
        for sublist in second_item:
            item, old_style_list = convert_old_style_list(sublist)
            if not old_style_list:
                break
            new_second_item.extend(item)
        if old_style_list:
            second_item = new_second_item
        return [first_item, second_item], old_style_list
    def _helper(list_):
        output = []
        list_length = len(list_)
        i = 0
        while i < list_length:
            title = list_[i]
            sublist = ''
            sublist_item = None
            if isinstance(title, (list, tuple)):
                sublist_item = title 
                title = ''
            elif i < list_length - 1:
                next_item = list_[i+1]
                if next_item and isinstance(next_item, (list, tuple)):
                    sublist_item = next_item
                    i += 1 
            if sublist_item:
                sublist = _helper(sublist_item)
                sublist = '<ul>%s</ul>' % sublist
            output.append('<li>%s%s</li>' % (strip_tags(force_unicode(title)), sublist))
            i += 1
        return '\n'.join(output)
    value, converted = convert_old_style_list(value) 
    return _helper(value)
register.filter(simple_unordered_list)

def include_admin_script(script_path):
    if not absolute_url_re.match(script_path):
        script_path = os.path.join(settings.MEDIA_PREFIX, script_path)
        if not script_path.startswith('/'):
            script_path = '/%s' % script_path
    return u'<script type="text/javascript" src="%s"></script>' % script_path
include_admin_script = register.simple_tag(include_admin_script)
