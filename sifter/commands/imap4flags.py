from email.message import Message

from sifter.grammar.command import Command
from sifter.validators.stringlist import StringList
from sifter.grammar.string import expand_variables
from sifter.grammar.state import EvaluationState

# This implements the RFC5232 imap4flags extension
# commands: addflag, removeflag, setflag
# tests: :hasflag
# tagged arguments: :flag to 'fileinto'


class CommandSetFlag(Command):

    HANDLER_ID = 'SETFLAG'
    EXTENSION_NAME = 'imap4flags'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = self.positional_args[0]
        flag_list = list(map(lambda s: expand_variables(s, state), flag_list))  # type: ignore
        state.actions.append('setflag', flag_list)


class CommandRemoveFlag(Command):

    HANDLER_ID = 'REMOVEFLAG'
    EXTENSION_NAME = 'imap4flags'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = self.positional_args[0]
        flag_list = list(map(lambda s: expand_variables(s, state), flag_list))  # type: ignore
        state.actions.append('removeflag', flag_list)


class CommandAddFlag(Command):

    HANDLER_ID = 'ADDFLAG'
    EXTENSION_NAME = 'imap4flags'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.check_required_extension('imap4flags', 'imapflags')
        flag_list = self.positional_args[0]
        flag_list = list(map(lambda s: expand_variables(s, state), flag_list))  # type: ignore
        state.actions.append('addflag', flag_list)
