from email.message import Message
from typing import (
    Optional
)
from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState


# section 5.10
class TestTrue(Test):

    RULE_IDENTIFIER = 'TRUE'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return True
