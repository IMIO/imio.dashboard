# -*- coding: utf-8 -*-
"""Installer for the imio.dashboard package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() + '\n\n' + open('CHANGES.rst').read() + '\n')

setup(
    name='imio.dashboard',
    version='0.29',
    description="This package is the glue between different packages "
                "offering a usable and integrated dashboard application",
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
        'Products.ZCatalog >= 3.1',
        'plone.api',
        # version 1.0.3+ manage correctly orphans
        'plone.batching > 1.0.4',
        'setuptools',
        'collective.behavior.talcondition',
        'collective.compoundcriterion',
        'collective.documentgenerator',
        'collective.eeafaceted.collectionwidget > 0.2',
        'collective.eeafaceted.z3ctable > 0.15',
        'collective.js.iframeresizer',
        'eea.facetednavigation < 10.0',
        'imio.actionspanel',
        'imio.migrator',
        'imio.prettylink',
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
