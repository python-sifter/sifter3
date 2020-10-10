from email.message import Message

from sifter.grammar.command import Command
from sifter.grammar.state import EvaluationState


# section 4.3
class CommandKeep(Command):

    HANDLER_ID = 'KEEP'
    HAS_BLOCKS = False

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.actions.append('keep')
        state.actions.cancel_implicit_keep()
