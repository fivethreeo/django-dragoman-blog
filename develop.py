#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hvad_blog
from djeasytests.testsetup import TestSetup

settings = {
    'DEBUG': True,
    'SITE_ID': 1,
    'STATIC_URL': '/static/', 
    'INSTALLED_APPS': [
        'hvad_blog_test_project',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.sites',
        'hvad_blog',
        'taggit',
        'hvad'
    ],
    'ROOT_URLCONF': 'hvad_blog_test_project.urls',
    'LANGUAGE_CODE': 'en',
    'LANGUAGES': (
        ('en', 'English'),
        ('ja', u'日本語')
    )
}
    
testsetup = TestSetup(appname='hvad_blog', test_settings=settings, version=hvad_blog.get_version())

if __name__ == '__main__':
    testsetup.run(__file__)
