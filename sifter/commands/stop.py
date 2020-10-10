from email.message import Message

from sifter.grammar.command import Command
from sifter.grammar.state import EvaluationState


# section 3.3
class CommandStop(Command):

    HANDLER_ID = 'STOP'

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.actions.append('stop')
