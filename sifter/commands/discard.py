from email.message import Message

from sifter.grammar.state import EvaluationState
from sifter.grammar.command import Command


# section 4.4
class CommandDiscard(Command):

    HANDLER_ID = 'DISCARD'

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.actions.cancel_implicit_keep()
