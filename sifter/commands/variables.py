import re
from email.message import Message
from typing import (
    Text
)

from urllib.parse import quote
from sifter.grammar.command import Command
from sifter.grammar.rule import RuleSyntaxError
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Tag
from sifter.grammar.string import expand_variables
from sifter.grammar.state import EvaluationState


# RFC 5229
class CommandSet(Command):

    HANDLER_ID = 'SET'
    EXTENSION_NAME = 'variables'
    TAGGED_ARGS = {
        'lower': Tag('LOWER'),
        'upper': Tag('UPPER'),
        'lowerfirst': Tag('LOWERFIRST'),
        'upperfirst': Tag('UPPERFIRST'),
        'quotewildcard': Tag('QUOTEWILDCARD'),
        'quoteregex': Tag('QUOTEREGEX'),
        'encodeurl': Tag('ENCODEURL'),
        'length': Tag('LENGTH'),
    }
    POSITIONAL_ARGS = [
        StringList(length=1),
        StringList(length=1),
    ]

    def evaluate(self, message: Message, state: EvaluationState) -> None:
        state.check_required_extension('variables', 'VARIABLES')

        variable_modifier = self.tagged_args
        variable_name = self.positional_args[0][0]  # type: ignore
        if (not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', variable_name)):
            raise RuleSyntaxError("Illegal variable name '%s' encountered" % variable_name)
        variable_value: Text = self.positional_args[1][0]  # type: ignore

        variable_value = expand_variables(variable_value, state)
        if 'lower' in variable_modifier:
            variable_value = variable_value.lower()
        if 'upper' in variable_modifier:
            variable_value = variable_value.upper()
        if 'lowerfirst' in variable_modifier:
            variable_value = variable_value[:1].lower() + variable_value[1:]
        if 'upperfirst' in variable_modifier:
            variable_value = variable_value[:1].upper() + variable_value[1:]
        if 'quotewildcard' in variable_modifier:
            variable_value = variable_value.replace('*', '\\*')
            variable_value = variable_value.replace('?', '\\?')
            variable_value = variable_value.replace('\\', '\\\\')
        if 'quoteregex' in variable_modifier:
            variable_value = re.escape(variable_value)
        if 'encodeurl' in variable_modifier:
            variable_value = quote(variable_value, safe='-._~')
        if 'length' in variable_modifier:
            variable_value = "" + str(len(variable_value))
        state.named_variables[variable_name] = variable_value
