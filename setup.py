# -*- coding: utf-8 -*-
"""Installer for the imio.dashboard package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='imio.dashboard',
    version='0.3',
    description="This package is the glue between different packages offering a usable and integrated dashboard application",
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
        'plone.api',
        # version 1.0.3+ manage correctly orphans
        'plone.batching > 1.0.4',
        'setuptools',
        'collective.behavior.talcondition',
        'collective.compoundcriterion',
        'collective.eeafaceted.collectionwidget',
        'collective.eeafaceted.z3ctable',
        'imio.actionspanel',
        'imio.prettylink',
        'collective.js.iframeresizer',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
