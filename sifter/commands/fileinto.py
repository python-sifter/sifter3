from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.command import Command
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 4.1
class CommandFileInto(Command):

    RULE_IDENTIFIER = 'FILEINTO'
    POSITIONAL_ARGS = [StringList(length=1)]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        file_dest = self.positional_args[0]

        state.check_required_extension('fileinto', 'FILEINTO')
        state.actions.append('fileinto', file_dest)  # type: ignore
        state.actions.cancel_implicit_keep()
        return None


CommandFileInto.register()
