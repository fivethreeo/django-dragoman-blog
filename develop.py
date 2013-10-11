#!/usr/bin/env python

import sys
import os

from djeasytests.testsetup import TestSetup

settings = {
    'DATABASES' = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'hvad_blog.sqlite'
            }
        }
    }
    
testsetup = TestSetup(appname='hvad_blog', settings=settings)

if __name__ == '__main__':
    testsetup.run(__file__)
