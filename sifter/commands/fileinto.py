from email.message import Message
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Union,
    SupportsInt,
    Text
)

from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test


# section 4.1
class CommandFileInto(Command):

    RULE_IDENTIFIER = 'FILEINTO'
    POSITIONAL_ARGS = [StringList(length=1)]

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        block: Optional[CommandList] = None
    ) -> None:
        super().__init__(arguments, tests, block)
        self.file_dest = self.positional_args[0]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        state.check_required_extension('fileinto', 'FILEINTO')
        state.actions.append('fileinto', self.file_dest)  # type: ignore
        state.actions.cancel_implicit_keep()
        return None


CommandFileInto.register()
