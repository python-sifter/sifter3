from email.message import Message
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.actions import Actions
from sifter.grammar.state import EvaluationState
from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test


# section 4.4
class CommandDiscard(Command):

    RULE_IDENTIFIER = 'DISCARD'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.cancel_implicit_keep()
        return None


CommandDiscard.register()
