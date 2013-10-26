from setuptools import setup, find_packages
import os

import dragoman_blog

CLASSIFIERS = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
]

setup(
    name='django-dragoman-blog',
    version=dragoman_blog.get_version(),
    description='This is a multilanguage blog app for django',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Oyvind Saltvik',
    author_email='oyvind.saltvik@gmail.com',
    url='http://github.com/fivethreeo/django-dragoman-blog/',
    packages=find_packages(),
    package_data={
        'dragoman_blog': [
            'static/dragoman_blog/*',
            'locale/*/LC_MESSAGES/*',
        ]
    },
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    install_requires=['django-taggit'],
)
