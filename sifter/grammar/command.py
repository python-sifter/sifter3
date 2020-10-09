from email.message import Message
from typing import (
    TYPE_CHECKING,
    Text,
    Optional,
    List,
    Union,
    SupportsInt,
    Tuple,
    Dict
)

import sifter.grammar
from sifter.grammar.command_list import CommandList
from sifter.grammar.rule import Rule, RuleSyntaxError
import sifter.utils
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test


class Command(Rule):

    HANDLER_TYPE: Text = 'command'
    HAS_BLOCKS: bool = True
    BLOCKS_MAX: int = 0

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        block: Optional[CommandList] = None
    ) -> None:
        if block is None:
            self.block = CommandList()
        else:
            self.block = block
        super().__init__(arguments, tests)

    def __str__(self) -> Text:
        s = [super().__str__(), ]
        if len(self.block.commands) > 0:
            s.append("{\n")
            for command in self.block.commands:
                s.append(sifter.utils.indent_string(str(command), 2))
            s.append("}\n")
        return ''.join(s)

    def validate_block_size(self, max_commands: int) -> None:
        if len(self.block.commands) > max_commands:
            raise RuleSyntaxError(
                "%s takes no more than %d commands" % (self.HANDLER_ID, max_commands)
            )

    def validate(self) -> Tuple[
        Dict[Text, List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]],
        List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]
    ]:
        if self.HAS_BLOCKS:
            self.validate_block_size(max_commands=self.BLOCKS_MAX)
        return super().validate()

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        raise NotImplementedError
