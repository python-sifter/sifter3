from email.message import Message
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test


# section 3.3
class CommandStop(Command):

    RULE_IDENTIFIER = 'STOP'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.actions.append('stop')
        return None


CommandStop.register()
