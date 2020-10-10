#!/usr/bin/env python

from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="sifter3",
    version="0.2.6",
    author="Manfred Kaiser, Gary Peck",
    author_email="manfred.kaiser@logfile.at, gary@realify.com",
    url="https://sifter3.readthedocs.io/en/latest/",
    license="BSD",
    description='Parser/evaluator for the Sieve filtering language (RFC 5228) - Python3 version',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="sieve email filter parser",
    project_urls={
        'Source': 'https://github.com/manfred-kaiser/sifter3',
        'Tracker': 'https://github.com/manfred-kaiser/sifter3/issues',
    },
    python_requires='>= 3.6',
    install_requires=[
        'ply'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email :: Filters",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=("tests",)),
    package_data={
        "sifter": ['py.typed']
    },
    entry_points={
        'console_scripts': [
            'sifter = sifter.cli:main'
        ],
        'sifter_extensions': [
            # sifter commands
            'discard = sifter.commands.discard:CommandDiscard',
            'fileinto = sifter.commands.fileinto:CommandFileInto',
            'if = sifter.commands.if_cmd:CommandIf',
            'elseif = sifter.commands.if_cmd:CommandElsIf',
            'else = sifter.commands.if_cmd:CommandElse',
            'keep = sifter.commands.keep:CommandKeep',
            'notify = sifter.commands.notify:CommandNotify',
            'redirect = sifter.commands.redirect:CommandRedirect',
            'reject = sifter.commands.reject:CommandReject',
            'ereject = sifter.commands.reject:CommandEReject',
            'require = sifter.commands.require:CommandRequire',
            'set = sifter.commands.variables:CommandSet',
            'stop = sifter.commands.stop:CommandStop',
            # sifter tests
            'address = sifter.tests.address:TestAddress',
            'body = sifter.tests.body:TestBody',
            'allof = sifter.tests.allof:TestAllOf',
            'anyof = sifter.tests.anyof:TestAnyOf',
            'exists = sifter.tests.exists:TestExists',
            'header = sifter.tests.header:TestHeader',
            'false = sifter.tests.false:TestFalse',
            'not_test = sifter.tests.not_test:TestNot',
            'size = sifter.tests.size:TestSize',
            'true = sifter.tests.true:TestTrue',
            'valid_notify_method = sifter.tests.notify:TestValidNotifyMethod',
            'notify_method_capability = sifter.tests.notify:TestValidNotifyMethod',
            'ihave = sifter.tests.ihave:TestIHave',
            # sifter comparators
            'ascii_casemap = sifter.comparators.ascii_casemap:ComparatorASCIICasemap',
            'ascii_casemap_noi = sifter.comparators.ascii_casemap:ComparatorASCIICasemapnoi',
            'octed = sifter.comparators.octet:ComparatorOctet',
            # notification methods
            'mailto = sifter.notificationmethods.mailto:MailtoNotificationMethod',
        ]
    }
)
