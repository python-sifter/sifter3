Sifter3 - Sieve email filter (RFC 5228)
=======================================

Sifter3 is a Python 3 implementation of the Sieve email filter language (RFC 5228)


FEATURES
--------

-   Supports all of the base Sieve spec from RFC 5228, except for
    features still listed under TODO below
-   Extensions supported:

    -   regex (draft-ietf-sieve-regex-01)
    -   body (RFC 5173)
    -   variables (RFC 5229)
    -   enotify (RFC 5435, particularly the mailto method RFC 5436)
    -   imap4flags (RFC 5232: setflag, addflag, removeflag; not supported: hasflags, :flags)

-   compatible with the Python 2 version from https://github.com/garyp/sifter

INSTALL
-------


.. code-block:: bash

    pip install sifter3


EXAMPLE
-------

.. code-block:: python

    import email
    import sifter.parser
    rules = sifter.parser.parse_file(open('my_rules.sieve'))
    msg = email.message_from_file(open('an_email_to_me.eml'))
    msg_actions = rules.evaluate(msg)

In the above example, ``msg_actions`` is a
list of actions to apply to the email message. Each action is a tuple
consisting of the action name and action-specific arguments. It is up to
the caller to manipulate the message and message store based on the
actions returned.

COMMAND LINE
------------

.. code-block:: bash

    $ sifter tests/evaluation_1.rules tests/evaluation_1.msg
    [('redirect', 'acm@example.com')]


WARNINGS
--------

-   No thought has been given yet to hardening against malicious user
    input. The current implementation is aimed at users that are running
    their own sieve scripts.
-   The current implementation is not optimized for performance, though
    hopefully it's not too slow for normal inputs.

TODO
----

-   An example adaptor that provides Unix LDA behavior using sieve for
    filtering
-   Base spec features not yet implemented:

    -   encoded characters (section 2.4.2.4)
    -   multi-line strings (section 2.4.2)
    -   bracketed comments (section 2.3)
    -   message uniqueness (section 2.10.3)
    -   envelope test (section 5.4)
    -   handle message loops (section 10)
    -   limit abuse of redirect action (section
