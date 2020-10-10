from email.message import Message
from typing import (
    Text
)

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState


# section 5.2
class TestAllOf(Test):

    HANDLER_ID: Text = 'ALLOF'
    HAS_TESTS = False

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        # short-circuit evaluation if a test is false. the base standard does
        # not specify if all tests must be evaluated or in what order, but the
        # "ihave" extension requires short-circuit left-to-right evaluation
        # (RFC 5463, section 4). so we might as well do that.
        for test in self.tests:
            if not test.evaluate(message, state):
                return False
        return True
