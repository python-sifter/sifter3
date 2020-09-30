from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.state import EvaluationState
from sifter.grammar.test import Test


# section 5.6
class TestFalse(Test):

    RULE_IDENTIFIER = 'FALSE'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return False
