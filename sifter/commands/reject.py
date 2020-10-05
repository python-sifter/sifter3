from email.message import Message
from typing import (
    Text,
    Optional
)

from sifter.grammar.command import Command
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 3.2
class CommandReject(Command):

    RULE_IDENTIFIER: Text = 'REJECT'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        print(self.positional_args[0][0])
        state.actions.append('reject', self.positional_args[0][0])
        state.actions.cancel_implicit_keep()
        return None
