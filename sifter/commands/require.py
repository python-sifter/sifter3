from email.message import Message
from typing import (
    Text,
    Optional
)

from sifter.grammar.command import Command
from sifter.extensions import ExtensionRegistry
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions


# section 3.2
class CommandRequire(Command):

    RULE_IDENTIFIER: Text = 'REQUIRE'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        ext_name_list = self.positional_args[0]
        for ext_name in ext_name_list:  # type: ignore
            if not ExtensionRegistry.has_extension(ext_name):
                raise RuntimeError(
                    "Required extension '%s' not supported"
                    % ext_name
                )
            state.require_extension(ext_name)
        return None
