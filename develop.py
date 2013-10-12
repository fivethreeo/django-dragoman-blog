#!/usr/bin/env python

import hvad_blog
from djeasytests.testsetup import TestSetup

settings = {
    'DATABASES' = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'hvad_blog.sqlite'
            }
        }
    }
    
testsetup = TestSetup(appname='hvad_blog', settings=settings, version=hvad_blog.get_version())

if __name__ == '__main__':
    testsetup.run(__file__)
