from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.command import Command
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 4.3
class CommandKeep(Command):

    RULE_IDENTIFIER = 'KEEP'
    HAS_BLOCKS = False

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.append('keep')
        state.actions.cancel_implicit_keep()
        return None
