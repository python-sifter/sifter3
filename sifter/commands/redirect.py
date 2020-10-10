import email.utils
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
from sifter.grammar.rule import RuleSyntaxError
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.string import expand_variables

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test


# section 4.2
class CommandRedirect(Command):

    HANDLER_ID = 'REDIRECT'
    POSITIONAL_ARGS = [StringList(length=1)]

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        block: Optional[CommandList] = None
    ) -> None:
        super().__init__(arguments, tests, block)

        self.email_address = self.positional_args[0][0]  # type: ignore
        # TODO: section 2.4.2.3 constrains the email address to a limited
        # subset of valid address formats. need to check if python's
        # email.utils also uses this subset or if we need to do our own
        # parsing.
        realname, emailaddr = email.utils.parseaddr(self.email_address)
        if emailaddr == "":
            raise RuleSyntaxError(
                "REDIRECT destination not a valid email address: %s"
                % self.email_address
            )

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        email_address = expand_variables(self.email_address, state)
        state.actions.append('redirect', email_address)
        state.actions.cancel_implicit_keep()
