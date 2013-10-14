================
django-hvad-blog
================

A internationalized blog using django-hvad.

Todo: Docs can be found at http://django-hvad-blog.readthedocs.org/ 

Todo: Translation project at transifex: http://www.transifex.net/projects/p/django-hvad-blog/

django-easytests
-----------------

* put apps/projects in testing/
* reusable test utils for 3rd party in hvad_blog/test_utils/ if needed
* see requirements and develop.py
    
Todo:
-----

* tests
* docs
* work

django-cms integration
======================

App with apphook and plugins, replaced model with placeholder(s).
Abstract model + default model ala django-shop, hooks for model replacement.

django-taggit-classy-templatetags
=================================

* rename module, taggit_classy
* design decisions and needs new tests
* use django-easytests
    
translated tags using taggit
============================

* add a language arg to templatetag?
* needs tests

To join in development
----------------------

::

    git clone https://github.com/fivethreeo/django-hvad-blog.git
    cd django-hvad-blog
    
    virtualenv --system-site-packages env
    env/bin/activate
    pip install -r testing/requirements/django-1.5.txt
    
    python develop.py test
    
    python develop.py manage syncdb --noinput
    python develop.py server
    
    http://127.0.0.1:8000/admin/
