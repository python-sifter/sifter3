from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.command import Command
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 3.3
class CommandStop(Command):

    HANDLER_ID = 'STOP'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.append('stop')
        return None
