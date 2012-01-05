#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

VERSION = __import__('geodjangofla').__version__

import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='geodjangofla',
    version = VERSION,
    description='This software is a Django application to simplify management '\
                'of GEOFLA(R) datas of the IGN (french geographic institute).',
    packages=['geodjangofla',
              'geodjangofla.management',
              'geodjangofla.management.commands',
              'geodjangofla.migrations'
              ],
    author=u'Étienne Loks',
    author_email='etienne.loks@peacefrogs.net',
    license='BSD',
    long_description=read('README.rst'),
    zip_safe=False,
    install_requires = ['Django>=1.2',
                        'south>=0.7.3',],
)


