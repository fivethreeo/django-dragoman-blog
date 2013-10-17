.. image:: https://travis-ci.org/fivethreeo/django-dragoman-blog.png?branch=develop
    :target: https://travis-ci.org/fivethreeo/django-dragoman-blog

====================
django-dragoman-blog
====================

A internationalized blog.

Todo: Docs can be found at http://django-dragoman-blog.readthedocs.org/ 

Todo: Translation project at transifex: http://www.transifex.net/projects/p/django-dragoman-blog/

Installation
------------

For the current stable version:

::

    pip install django-dragoman-blog # no pypi yet

For the development version:

::

    pip install -e git+git://github.com/fivethreeo/django-dragoman-blog.git@develop#egg=django-dragoman-blog

Configuration
-------------

Settings
========

Add ::

    'dragoman_blog',
    'taggit',

To INSTALLED_APPS.

Set MIDDLEWARE_CLASSES to ::

    (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware'
    )

Urls
====

Add ::
    
    from django.conf.urls.i18n import i18n_patterns
    
    urlpatterns += i18n_patterns('',
        url(r'^blog/', include('dragoman_blog.urls'))
    )

To your project roots urls.py


To join in development
----------------------

::

    git clone https://github.com/fivethreeo/django-dragoman-blog.git
    cd django-dragoman-blog
    
    virtualenv --system-site-packages env
    env/bin/activate
    pip install -r testing/requirements/django-1.5.txt
    
    python develop.py test
    
    python develop.py manage syncdb --noinput
    python develop.py server
    
    http://127.0.0.1:8000/admin/
    
django-easytests
================

* put apps/projects in testing/
* reusable test utils for 3rd party in dragoman_blog/test_utils/ if needed
* see develop.py

Todo:
=====

* tests
* docs
* work

django-cms integration
''''''''''''''''''''''

App with apphook and plugins, replaced model with placeholder(s).
Abstract model + default model ala django-shop, hooks for model replacement.

django-taggit-classy-templatetags
'''''''''''''''''''''''''''''''''

* rename module, taggit_classy
* needs new tests
    
translated tags using taggit
''''''''''''''''''''''''''''

* needs tests, views and templatetags
    
