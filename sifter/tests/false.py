from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.state import EvaluationState
from sifter.grammar.test import Test

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String


# section 5.6
class TestFalse(Test):

    RULE_IDENTIFIER = 'FALSE'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[bool]:
        return False


TestFalse.register()
