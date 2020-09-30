from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.actions import Actions
from sifter.grammar.state import EvaluationState
from sifter.grammar.command import Command


# section 4.4
class CommandDiscard(Command):

    RULE_IDENTIFIER = 'DISCARD'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.cancel_implicit_keep()
        return None
