from email.message import Message
from typing import (
    Text
)

from sifter.grammar.command import Command
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState


# section 3.2
class CommandReject(Command):

    HANDLER_ID: Text = 'REJECT'
    EXTENSION_NAME = 'reject'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        reject_message = self.positional_args[0][0]  # type: ignore
        state.actions.append('reject', reject_message)
        state.actions.cancel_implicit_keep()


class CommandEReject(CommandReject):

    HANDLER_ID: Text = 'EREJECT'
    EXTENSION_NAME = 'ereject'
