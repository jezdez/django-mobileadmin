from django.contrib.admin import site as main_site
from django.core.exceptions import ImproperlyConfigured

from mobileadmin import decorators, views
from mobileadmin.conf import settings

### From http://www2.lib.uchicago.edu/keith/courses/python/class/5/#attrref
def classlookup(C, name):
	if C.__dict__.has_key(name):
		return (1, C.__dict__[name])
	else:
		for b in C.__bases__:
		    success, value = classlookup(b, name)
		    if success:
			    return (1, value)
		    else:
			    pass
		else:
		    return (0, None)


def autoregister():
    """
    Auto-register all ModelAdmin instances of the default AdminSite with the
    mobileadmin app and set the templates accordingly.
    """
    from django.contrib.auth.admin import UserAdmin
    from mobileadmin.sites import site
    
    for model, modeladmin in main_site._registry.iteritems():
        admin_class = modeladmin.__class__
        for name in settings.TEMPLATE_MAPPING:
            (found, value) = classlookup(admin_class, name)
            if found:
                setattr(admin_class, name, decorators.mobile_templates(value))
                
        if admin_class == UserAdmin:
            setattr(admin_class, 'add_view', views.auth_add_view)

        site.register(model, admin_class)

def autodiscover():
        raise ImproperlyConfigured("Please use the autodiscover function of "
                                   "Django's default admin app and then "
                                   "call 'mobileadmin.autoregister' to use "
                                   "mobileadmin.")
