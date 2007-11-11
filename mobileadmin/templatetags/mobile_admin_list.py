from django import template
from django.contrib.admin.views.main import ALL_VAR, PAGE_VAR, SEARCH_VAR

register = template.Library()

def paginator_number(cl, i):
    if i == cl.page_num:
        classname = "active"
    else:
        classname = "inactive"
    return u'<a href="%s" class="%s float-left">%d</a> ' % (cl.get_query_string({PAGE_VAR: i}), classname, i+1)
paginator_number = register.simple_tag(paginator_number)

def pagination(cl):
    paginator, page_num = cl.paginator, cl.page_num

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 1

        # If there are 4 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.pages <= 3:
            page_range = range(paginator.pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > ON_EACH_SIDE:
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.pages - ON_EACH_SIDE - 1):
                page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.extend(range(paginator.pages, paginator.pages))
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

def search_form(cl):
    return {
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count and not cl.opts.one_to_one_field,
        'search_var': SEARCH_VAR
    }
search_form = register.inclusion_tag('admin/search_form.html')(search_form)

def filter(cl, spec):
    return {
        'title': spec.title(),
        'choices' : list(spec.choices(cl))
    }
filter = register.inclusion_tag('admin/filter.html')(filter)
