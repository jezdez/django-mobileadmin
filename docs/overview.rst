=============================================
The Django admin interface for mobile devices
=============================================

.. contents::
    :backlinks: none

This is an alternative admin interface for Django for use with mobile devices
such as the iPhone/iPod touch or Blackberry. Some would call it a theme or a
skin, but actually it's more than that.

It resembles almost all features of the regular Django admin interface and
brings everything you need to add support for arbitrary devices.

I hope you like it.

Download & Installation
=======================

Get the source from the application site at::

    http://code.google.com/p/django-mobileadmin/

To install the *mobileadmin*, follow these steps:

1. Follow the instructions in the INSTALL.txt file
2. Add ``'mobileadmin'`` to the INSTALLED_APPS_ setting of your Django site.
   That might look like this::
   
    INSTALLED_APPS = (
       # ...
       'mobileadmin',
    )
   
3. Make sure you've installed_ the admin contrib app.
4. Add ``'mobileadmin.context_processors.user_agent'`` to your 
   TEMPLATE_CONTEXT_PROCESSORS_ setting. It should look like this::
   
    TEMPLATE_CONTEXT_PROCESSORS = (
       'django.core.context_processors.auth',
       'django.core.context_processors.debug',
       'django.core.context_processors.i18n',
       'django.core.context_processors.media',
       'django.core.context_processors.request',
       'mobileadmin.context_processors.user_agent',
    )

Usage
=====

Since *mobileadmin* follows the ideas of Django's admin interface you can
easily reuse your existing admin setup:

You use the default or custom ModelAdmin classes for each model you wanted
to be editable in the admin interface and hooked up Django's default
AdminSite instance with your URLconf.

If that's the case you are able to re-use those ModelAdmin (sub-)classes
by using *mobileadmin*'s separate admin site instance and its autoregister()
function.

1.  In your root URLconf -- just **below** the line where Django's
    admin.autodiscover() gets called -- import ``mobileadmin`` and call the
    function ``mobileadmin.autoregister()``::

        # urls.py
        from django.conf.urls.defaults import *
        from django.contrib import admin

        admin.autodiscover()

        import mobileadmin
        mobileadmin.autoregister()

        urlpatterns = patterns('',
            ('^admin/(.*)', admin.site.root),
        )
    
    This registers your existing admin configuration with *mobileadmin*.

2.  Extend the urlpatterns to hook the default ``MobileAdminSite`` instance`
    with your favorite URL, e.g. ``/ma/``. Add::

        urlpatterns += patterns('',
            (r'^ma/(.*)', mobileadmin.sites.site.root),
        )
        
    *mobileadmin* is now replicating all of the regular admin features and
    uses templates adapted to the mobile device you are using.

3.  Set the ``handler404`` and ``handler500`` variables in your URLConf to the
    views that are provided by *mobileadmin*::

        handler404 = 'mobileadmin.views.page_not_found'
        handler500 = 'mobileadmin.views.server_error'
    
    That is needed to load the ``404.html`` and ``500.html`` templates
    according to the user agent of the browser on your mobile device. It
    has an automatic fallback to `Django's default error handlers`_.

.. _INSTALLED_APPS: http://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
.. _ADMIN_MEDIA_PREFIX: http://docs.djangoproject.com/en/dev/ref/settings/#admin-media-prefix
.. _TEMPLATE_CONTEXT_PROCESSORS: http://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
.. _installed: http://docs.djangoproject.com/en/dev/ref/contrib/admin/#overview
.. _Django's default error handlers: http://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views

Extending ``mobileadmin``
=========================

*mobileadmin* comes with a default set of templates and patterns to
recognize different devices and platforms:

- Mobile Safari (iPhone/iPod touch)
- Blackberry
- Opera Mini

But it's made for being extended.

Since the template loading depends on the user agent of the requesting client,
*mobileadmin* tells Django to look for three templates, when trying to render
one of the default admin views:

1. ``mobileadmin/USER_AGENT_NAME/VIEW_TEMPLATE.html``
2. ``mobileadmin/VIEW_TEMPLATE.html``
3. ``admin/index.html``

..where:
    
- ``USER_AGENT`` is the short name of the user agent
- ``VIEW_TEMPLATE`` is the name of the rendered template

If you would try to access the login view with the iPhone for example, the
following three templates would be tried to load:

1. ``mobileadmin/mobile_safari/login.html``
2. ``mobileadmin/login.html``
3. ``admin/index.html``

..where ``mobile_safari`` is the name of one of the default device patterns
and ``login.html`` the name of the to needed template.

Creating a custom ``mobileadmin`` setup
---------------------------------------

You can add support for more user agents by adding ``MOBILEADMIN_USER_AGENTS``
to your settings.py file -- consisting of a short name and a regualar
expression, matching that user agent string::

    MOBILEADMIN_USER_AGENTS = {
        'my_user_agent': r'.*MyUserAgent.*',
    }

With that it would automatically check if the regular expression matches with
the user agent of the current request and -- if yes -- try to load the
templates ``mobileadmin/my_user_agent/login.html``, when accessing the the
login page -- falling back to ``my_user_agent/login.html`` and later to
``admin/login.html``, if not found.

Have a look at ``TEMPLATE_MAPPING`` in ``mobileadmin/conf/settings.py``
if you want to know the default regular expressions.

*mobileadmin* comes with a ``MobileAdminSite`` and a ``MobileModelAdmin``
class that uses the default ``TEMPLATE_MAPPING`` and ``USER_AGENTS``
settings out of the box::

    from mobileadmin import sites
    
    class MyMobileAdminSite(sites.MobileAdminSite):
        # define here whatever function you want
        pass

But if you want to use the ability of *mobileadmin* to change the template
depending on the user agent, you need to modify a bit of your admin classes.

Luckily *mobileadmin* comes with a decorator to be used on ``AdminSite`` or
``ModelAdmin`` methods that changes the template of that method according to
the current user agent by using a template mapping, which can be found in
``mobileadmin/conf/settings.py`` in the ``TEMPLATE_MAPPING`` variable.

Those mappings are used by the decorator ``mobile_templates`` that applies
them on the corresponding methods of your own ``AdminSite`` or
``ModelAdmin``, e.g.::

    from django.contrib.admin import sites
    from mobileadmin.decorators import mobile_templates
    
    class MyAdminSite(sites.AdminSite):
        
        def index(self, request, extra_context=None):

            # self.index_template is already automatically set here
            # do something cool here
            
            return super(MyAdminSite, self).index(request, extra_context)
        index = mobile_templates(index)

Furthermore the default mappings can be extended in your site settings.py::

    MOBILEADMIN_TEMPLATE_MAPPING = {
        'index': ('index_template', 'index.html'),
    }

..where:

- ``index`` is the name of the function, whose class attribute and
- ``index_template`` (an attribute of the method's class) would be set to the
  the file ``index.html``.

Using custom mobile admin interfaces
------------------------------------

In case you created your own mobile admin interface, you can use
*mobileadmin*'s subclasses of Django's `ModelAdmin`_, `InlineModelAdmin`_
and `AdminSite`_ classes, that include the neccesary bits to make it work.

Just use it as you would use the base classes, e.g.::

    from mobileadmin import options
    from myproject.myapp.models import Author

    class MobileAuthorAdmin(options.MobileModelAdmin):
        pass
    mobileadmin.sites.site.register(Author, MobileAuthorAdmin)

Then import ``mobileadmin`` in your URLconf to instantiate a
``MobileAdminSite`` object, use Django's ``autodiscover()`` to load
``INSTALLED_APPS`` admin.py modules and add an URL for the *mobileadmin* to
the URLConf::

    # urls.py
    from django.conf.urls.defaults import *
    from django.contrib import admin
    import mobileadmin

    admin.autodiscover()

    urlpatterns = patterns('',
        ('^admin/(.*)', admin.site.root),
        (r'^ma/(.*)', mobileadmin.sites.site.root),
    )

.. _InlineModelAdmin: http://docs.djangoproject.com/en/dev/ref/contrib/admin/#inlinemodeladmin-objects
.. _AdminSite: http://docs.djangoproject.com/en/dev/ref/contrib/admin/#adminsite-objects
.. _ModelAdmin: http://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-objects

Media path
==========

Please feel free to use some nice little helpers to find the path to
*mobileadmin*'s media directory. If you are using Django (or any other Python
software) to serve static files (which you shouldn't in production) just use
for example::

    from mobileadmin.conf import settings

    mobileadmin_media_path = settings.MEDIA_PATH
    mobileadmin_media_prefix = settings.MEDIA_PREFIX

You now have the full (platform-independent) path to the media directory of
*mobileadmin* in the variable ``mobileadmin_media_path`` and the default URL
prefix (``'/mobileadmin_media/'``) for the *mobileadmin* media -- CSS, Javascript
and images -- in ``mobileadmin_media_prefix``. Just like the
ADMIN_MEDIA_PREFIX_ but for the ``media`` directory of the *mobileadmin* app.

You can of course optionally override the default URL prefix by setting
a ``MOBILEADMIN_MEDIA_PREFIX`` in the settings.py file of your Django site.
Please use a trailing slash. This makes updating *mobileadmin* much easier for
you, since you now don't have to bother about different locations of the media
directory. 

Serving *mobileadmin*'s static media
------------------------------------

Even though using Django's ability to serve static files is strongly **NOT
RECOMMENDED** for live production servers, it might be helpful to bring up
*mobileadmin* for a test drive or an intranet website. Just add the following
code to the URLConf (``urls.py``) of your Django site::

    from mobileadmin.conf import settings
    
    urlpatterns += patterns('django.views.static',
        (settings.MEDIA_REGEX, 'serve', {'document_root': settings.MEDIA_PATH}),
    )

See how *mobileadmin*'s own settings module is loaded at the top of the snippet
that enables you to obtain a ready-made regex for the static files
(``MEDIA_REGEX``) and the platform-independent filesystem path to the media
files (``MEDIA_PATH``).

Support
=======

Please leave your `questions and problems`_ on the `designated Google Code site`_.

.. _designated Google Code site: http://code.google.com/p/django-mobileadmin/
.. _questions and problems: http://code.google.com/p/django-mobileadmin/issues/
