import sifter.commands.discard
import sifter.commands.fileinto
import sifter.commands.rewrite
import sifter.commands.imap4flags
import sifter.commands.if_cmd
import sifter.commands.keep
import sifter.commands.redirect
import sifter.commands.require
import sifter.commands.stop
import sifter.commands.variables
import sifter.commands.pipe
import sifter.commands.notify

import sifter.tests.address
import sifter.tests.allof
import sifter.tests.anyof
import sifter.tests.exists
import sifter.tests.header
import sifter.tests.body
import sifter.tests.envelope
import sifter.tests.false
import sifter.tests.not_test
import sifter.tests.size
import sifter.tests.true
import sifter.tests.notify

import sifter.comparators.ascii_casemap
import sifter.comparators.octet

import sifter.notificationmethods.mailto

import sifter.extension
list(map(sifter.extension.register,
    ('fileinto',
     'comparator-i;ascii-casemap',
     'comparator-i;octet',
     'rewrite',
     'body',
     'variables',
     'enotify',
     'pipe',
     'envelope'
     )))
