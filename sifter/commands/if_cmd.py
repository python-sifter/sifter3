from email.message import Message
from typing import (
    Optional
)

from sifter.grammar.command import Command
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 3.1
class CommandIfBase(Command):

    TESTS_MIN = 1
    HAS_BLOCKS = False

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if self.tests[0].evaluate(message, state):
            result = self.block.evaluate(message, state)
            state.last_if = True
            return result
        state.last_if = False
        return None


class CommandIf(CommandIfBase):

    RULE_IDENTIFIER = 'IF'


class CommandElsIf(CommandIfBase):

    RULE_IDENTIFIER = 'ELSIF'

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if state.last_if:
            return None
        return super().evaluate(message, state)


class CommandElse(Command):

    RULE_IDENTIFIER = 'ELSE'
    TESTS_MIN = 0
    HAS_BLOCKS = False

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        if state.last_if:
            return None
        return self.block.evaluate(message, state)
