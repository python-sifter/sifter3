from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.command import Command
from sifter.grammar.string import expand_variables
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 4.1
class CommandFileInto(Command):

    RULE_IDENTIFIER = 'FILEINTO'
    POSITIONAL_ARGS = [StringList(length=1)]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.check_required_extension('fileinto', 'FILEINTO')

        file_dest = self.positional_args[0]
        file_dest = list(map(lambda s: expand_variables(s, state), file_dest))  # type: ignore

        state.actions.append('fileinto', file_dest)
        state.actions.cancel_implicit_keep()
        return None
