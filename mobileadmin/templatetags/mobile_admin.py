from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.contrib.admin.views.main import ALL_VAR
from django.contrib.admin.views.main import PAGE_VAR

DOT = '.'

register = template.Library()

def mobileadmin_media_prefix():
    if settings.MOBILEADMIN_MEDIA_PREFIX:
        return settings.MOBILEADMIN_MEDIA_PREFIX
    return ''
mobileadmin_media_prefix = register.simple_tag(mobileadmin_media_prefix)

def get_app_model_url(cl):
    return "%s/%s/" % (cl.opts.app_label, cl.opts.object_name.lower())
get_app_model_url = register.simple_tag(get_app_model_url)

def get_result_url(cl, res):
    """
    Returns the url of a specific result from a change list
    """
    return "%s/%s/%s" % (cl.opts.app_label, cl.opts.object_name.lower(), cl.url_for_result(res))
get_result_url = register.simple_tag(get_result_url)

def get_admin_root():
    try:
        admin_url = reverse('django.contrib.admin.views.main.index')
    except NoReverseMatch:
        admin_url = None
    return admin_url
get_admin_root = register.simple_tag(get_admin_root)

def get_content_type(model):
    """
    Returns the url of a specific result from a change list
    """
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(model).id
get_content_type = register.simple_tag(get_content_type)

def truncate(value, size):
    return value[0:size]
register.filter(truncate)

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

def paginator_number(cl,i):
    if i == DOT:
        return u'... '
    elif i == cl.page_num:
        return u'<span class="text">%d</span> ' % (i+1)
    else:
        return u'<a href="%s" class="inactive">%d</a> ' % (cl.get_query_string({PAGE_VAR: i}), i+1)
paginator_number = register.simple_tag(paginator_number)

def pagination(cl):
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.pages <= 10:
            page_range = range(paginator.pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.pages - ON_ENDS, paginator.pages))
            else:
                page_range.extend(range(page_num + 1, paginator.pages))

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    }
pagination = register.inclusion_tag('admin/pagination.html')(pagination)