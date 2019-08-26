#!/usr/bin/env python
# vim: sw=4 ts=4 et si:

import sifter.grammar
import sifter.validators
import sifter.extension

# This implements the RFC5232 imap4flags extension
# commands: addflag, removeflag, setflag
# tests: :hasflag
# tagged arguments: :flag to 'fileinto'

__all__ = ('CommandSetFlag', 'CommandAddFlag', 'CommandRemoveFlag')

class CommandSetFlag(sifter.grammar.Command):
    RULE_IDENTIFIER = 'SETFLAG'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandSetFlag, self).__init__(arguments, tests,block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(), ],
        )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.flag_list = positional_args[0]

    def evaluate(self, message, state):
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.flag_list)
        state.actions.append('setflag', flag_list)
CommandSetFlag.register()

class CommandRemoveFlag(sifter.grammar.Command):
    RULE_IDENTIFIER = 'REMOVEFLAG'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandRemoveFlag, self).__init__(arguments, tests,block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(), ],
        )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.flag_list = positional_args[0]

    def evaluate(self, message, state):
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.flag_list)
        state.actions.append('removeflag', flag_list)

CommandRemoveFlag.register()

class CommandAddFlag(sifter.grammar.Command):
    RULE_IDENTIFIER = 'ADDFLAG'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandAddFlag, self).__init__(arguments, tests,block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(), ],
        )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.flag_list = positional_args[0]

    def evaluate(self, message, state):
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.flag_list)
        state.actions.append('addflag', flag_list)

CommandAddFlag.register()

sifter.extension.register('imap4flags')
