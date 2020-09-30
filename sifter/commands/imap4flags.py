from email.message import Message
from typing import Optional

from sifter.grammar.command import Command
from sifter.validators.stringlist import StringList
from sifter.grammar.string import expand_variables
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

# This implements the RFC5232 imap4flags extension
# commands: addflag, removeflag, setflag
# tests: :hasflag
# tagged arguments: :flag to 'fileinto'


class CommandSetFlag(Command):

    RULE_IDENTIFIER = 'SETFLAG'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = self.positional_args[0]
        flag_list = list(map(lambda s: expand_variables(s, state), flag_list))  # type: ignore
        state.actions.append('setflag', flag_list)
        return None


class CommandRemoveFlag(Command):

    RULE_IDENTIFIER = 'REMOVEFLAG'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = self.positional_args[0]
        flag_list = list(map(lambda s: expand_variables(s, state), flag_list))  # type: ignore
        state.actions.append('removeflag', flag_list)
        return None


class CommandAddFlag(Command):

    RULE_IDENTIFIER = 'ADDFLAG'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = self.positional_args[0]
        flag_list = list(map(lambda s: expand_variables(s, state), flag_list))  # type: ignore
        state.actions.append('addflag', flag_list)
        return None
