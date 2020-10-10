# Sifter3 - Sieve email filter (RFC 5228)

Sifter3 is a Python 3 implementation of the Sieve email filter language (RFC 5228)

![Python package](https://github.com/manfred-kaiser/sifter3/workflows/Python%20package/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/sifter3/badge/?version=latest)](https://sifter3.readthedocs.io/en/latest/?badge=latest)
[![CodeFactor](https://www.codefactor.io/repository/github/manfred-kaiser/sifter3/badge)](https://www.codefactor.io/repository/github/manfred-kaiser/sifter3)
[![Github version](https://img.shields.io/github/v/release/manfred-kaiser/sifter3?label=github&logo=github)](https://github.com/manfred-kaiser/sifter3/releases)
[![PyPI version](https://img.shields.io/pypi/v/sifter3.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/sifter3/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/sifter3.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/sifter3/)
[![PyPI downloads](https://pepy.tech/badge/sifter3/month)](https://pepy.tech/project/sifter3/month)
[![GitHub](https://img.shields.io/github/license/manfred-kaiser/sifter3.svg)](LICENSE)



FEATURES
========

-   Supports all of the base Sieve spec from RFC 5228, except for
    features still listed under TODO below
    -   multiline strings (since version 0.2.2)
    -   bracketed comments (since version 0.2.4)
-   Extensions supported:
    -   regex (draft-ietf-sieve-regex-01)
    -   body (RFC 5173)
    -   variables (RFC 5229)
    -   enotify (RFC 5435, particularly the mailto method RFC 5436)
    -   imap4flags (RFC 5232: setflag, addflag, removeflag; not supported: hasflags, :flags)
    -   reject and ereject (RFC 5429)
    -   ihave (RFC 5463)


INSTALL
=======

    pip install sifter3

EXAMPLE
=======

    import email
    import sifter.parser
    rules = sifter.parser.parse_file(open('my_rules.sieve'))
    msg = email.message_from_file(open('an_email_to_me.eml'))
    msg_actions = rules.evaluate(msg)

In the above example, `msg_actions` is a list of actions to apply to the
email message. Each action is a tuple consisting of the action name and
action-specific arguments. It is up to the caller to manipulate the
message and message store based on the actions returned.

COMMAND LINE
============

The output of the command line tool can be parsed as json.

    $ sifter tests/evaluation_1.rules tests/evaluation_1.msg
    [['redirect', 'acm@example.com']]


WARNINGS
========

-   No thought has been given yet to hardening against malicious user
    input. The current implementation is aimed at users that are running
    their own sieve scripts.
-   The current implementation is not optimized for performance, though
    hopefully it's not too slow for normal inputs.

TODO
====

-   An example adaptor that provides Unix LDA behavior using sieve for
    filtering
-   Base spec features not yet implemented:
    -   encoded characters (section 2.4.2.4)
    -   message uniqueness (section 2.10.3)
    -   envelope test (section 5.4)
    -   handle message loops (section 10)
    -   limit abuse of redirect action (section 10)
    -   address test should limit allowed headers to those that contain
        addresses (section 5.1)
-   Make sure character sets are actually handled according to the spec
-   Make string parsing comply with the grammar in section 8.1 and the
    features described in section 2.4.2
-   Check that python's `email.message` implements header comparisons
    the same way as the sieve spec
-   Make sure regular expressions are actually handled according to the
    extension spec
-   Add support for various extensions:
    -   externally stored lists (draft-melnikov-sieve-external-lists)
    -   relational (RFC 5231)
    -   subaddress (RFC 5233)
    -   copy (RFC 3894)
    -   environment (RFC 5183)
    -   date and index (RFC 5260)
    -   editheader (RFC 5293)
    -   mailbox metadata (RFC 5490)
    -   xmpp notifications (RFC 5437)
