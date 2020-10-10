from email.message import Message

from sifter.grammar.command import Command
from sifter.grammar.string import expand_variables
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState


# section 4.1
class CommandFileInto(Command):

    HANDLER_ID = 'FILEINTO'
    EXTENSION_NAME = 'fileinto'
    POSITIONAL_ARGS = [StringList(length=1)]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.check_required_extension('fileinto', 'FILEINTO')

        file_dest = self.positional_args[0]
        file_dest = list(map(lambda s: expand_variables(s, state), file_dest))  # type: ignore

        state.actions.append('fileinto', file_dest)
        state.actions.cancel_implicit_keep()
