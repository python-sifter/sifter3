from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.test import Test
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String


# section 5.8
class TestNot(Test):

    RULE_IDENTIFIER = 'NOT'
    TESTS_MIN = 1

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return not self.tests[0].evaluate(message, state)


TestNot.register()
