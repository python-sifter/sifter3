from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState


# section 5.8
class TestNot(Test):

    RULE_IDENTIFIER = 'NOT'
    TESTS_MIN = 1

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return not self.tests[0].evaluate(message, state)
