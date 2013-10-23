#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dragoman_blog
from djeasytests.testsetup import TestSetup

settings = {
    'DEBUG': True,
    'SITE_ID': 1,
    'STATIC_URL': '/static/', 
    'INSTALLED_APPS': [
        'dragoman_blog_test_project',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.sites',
        'dragoman_blog',
        'taggit',
    ],
    'USE_TZ': True,
    'MIDDLEWARE_CLASSES': (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    'ROOT_URLCONF': 'dragoman_blog_test_project.urls',
    'LANGUAGE_CODE': 'en',
    'LANGUAGES': (
        ('en', 'English'),
        ('ja', u'日本語')
    )
}
    
testsetup = TestSetup(appname='dragoman_blog', test_settings=settings, version=dragoman_blog.get_version())

if __name__ == '__main__':
    testsetup.run(__file__)
