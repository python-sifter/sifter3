from email.message import Message

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState


# section 5.10
class TestTrue(Test):

    HANDLER_ID = 'TRUE'

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        return True
