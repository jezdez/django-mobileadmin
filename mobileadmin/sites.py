from django.contrib.admin import sites
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import password_change, password_change_done, logout

from mobileadmin.decorators import mobile_templates

class MobileAdminSite(sites.AdminSite):
    """
    A custom admin site to override the used templates.
    Add that to your urls.py:
    
    import mobileadmin
    urlpatterns += patterns('',
        (r'^m/(.*)', include(mobileadmin.sites.site.urls)),
    )
    """
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    def index(self, request, extra_context=None):
        return super(MobileAdminSite, self).index(request, extra_context)
    index = mobile_templates(index)
    
    def display_login_form(self, request, error_message='', extra_context=None):
        return super(MobileAdminSite, self).display_login_form(request, error_message, extra_context)
    display_login_form = mobile_templates(display_login_form)

    def app_index(self, request, app_label, extra_context=None):
        return super(MobileAdminSite, self).app_index(request, app_label, extra_context)
    app_index = mobile_templates(app_index)

    def logout(self, request):
        return logout(request, template_name=self.logout_template or 'registration/logged_out.html')
    logout = never_cache(mobile_templates(logout))

    def password_change(self, request):
        return password_change(request,
            template_name=self.password_change_template or 'registration/password_change_form.html',
            post_change_redirect='%spassword_change/done/' % self.root_path)
    password_change = mobile_templates(password_change)

    def password_change_done(self, request):
        return password_change_done(request,
            template_name=self.password_change_done_template or 'registration/password_change_done.html')
    password_change_done = mobile_templates(password_change_done)

site = MobileAdminSite()
