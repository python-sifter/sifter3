import re
from urllib.parse import quote
from sifter.grammar.command import Command
from sifter.grammar.rule import RuleSyntaxError
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Tag
from sifter.grammar.string import expand_variables

__all__ = ('CommandSet',)


# RFC 5229
class CommandSet(Command):

    RULE_IDENTIFIER = 'SET'
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

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandSet, self).__init__(arguments, tests, block)

        self.variable_modifier = self.tagged_args
        self.variable_name = self.positional_args[0][0]
        if (not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', self.variable_name)):
            raise RuleSyntaxError("Illegal variable name '%s' encountered" % self.variable_name)
        self.variable_value = self.positional_args[1][0]

    def evaluate(self, message, state):
        state.check_required_extension('variables', 'VARIABLES')
        variable_value = expand_variables(self.variable_value, state)
        if 'lower' in self.variable_modifier:
            variable_value = variable_value.lower()
        if 'upper' in self.variable_modifier:
            variable_value = variable_value.upper()
        if 'lowerfirst' in self.variable_modifier:
            variable_value = variable_value[:1].lower() + variable_value[1:]
        if 'upperfirst' in self.variable_modifier:
            variable_value = variable_value[:1].upper() + variable_value[1:]
        if 'quotewildcard' in self.variable_modifier:
            variable_value = variable_value.replace('*', '\\*')
            variable_value = variable_value.replace('?', '\\?')
            variable_value = variable_value.replace('\\', '\\\\')
        if 'quoteregex' in self.variable_modifier:
            variable_value = re.escape(variable_value)
        if 'encodeurl' in self.variable_modifier:
            variable_value = quote(variable_value, safe='-._~')
        if 'length' in self.variable_modifier:
            variable_value = "" + len(variable_value)
        state.named_variables[self.variable_name] = variable_value
