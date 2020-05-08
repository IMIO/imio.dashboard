# -*- coding: utf-8 -*-
"""Installer for the imio.dashboard package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() + '\n\n' + open('CHANGES.rst').read() + '\n')

setup(
    name='imio.dashboard',
    version='2.7',
    description="This package adds functionnality to collective.eeafaceted.dashboard "
                "but only work for Plone 4.3.x",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Zope Plone',
    author='IMIO',
    author_email='dev@imio.be',
    url='http://pypi.python.org/pypi/imio.dashboard',
    license='GPL V2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['imio'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.eeafaceted.batchactions',
        'collective.eeafaceted.dashboard',
        'collective.js.iframeresizer',
        'imio.actionspanel',
        'imio.migrator',
    ],
    extras_require={
        'test': [
            'imio.helpers',
            'plone.app.dexterity',
            'plone.app.testing',
            'plone.app.relationfield',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
