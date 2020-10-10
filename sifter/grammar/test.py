from email.message import Message

from sifter.grammar.rule import Rule
from sifter.grammar.state import EvaluationState


class Test(Rule):

    HANDLER_TYPE = 'test'

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        raise NotImplementedError
