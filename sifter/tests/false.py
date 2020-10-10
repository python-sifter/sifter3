from email.message import Message

from sifter.grammar.state import EvaluationState
from sifter.grammar.test import Test


# section 5.6
class TestFalse(Test):

    HANDLER_ID = 'FALSE'

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        return False
