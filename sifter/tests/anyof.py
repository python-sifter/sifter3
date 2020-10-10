from email.message import Message

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState


# section 5.3
class TestAnyOf(Test):

    HANDLER_ID = 'ANYOF'
    HAS_TESTS = False

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        # short-circuit evaluation if a test is true. the base standard does
        # not specify if all tests must be evaluated or in what order, but the
        # "ihave" extension requires short-circuit left-to-right evaluation
        # (RFC 5463, section 4). so we might as well do that.
        for test in self.tests:
            if test.evaluate(message, state):
                return True
        return False
