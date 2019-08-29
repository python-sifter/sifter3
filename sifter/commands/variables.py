import re
import urllib
import sifter.grammar
import sifter.validators

__all__ = ('CommandSet',)

# RFC 5229
class CommandSet(sifter.grammar.Command):

    RULE_IDENTIFIER = 'SET'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandSet, self).__init__(arguments, tests, block)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'lower' : sifter.validators.Tag('LOWER'),
                    'upper' : sifter.validators.Tag('UPPER'),
                    'lowerfirst' : sifter.validators.Tag('LOWERFIRST'),
                    'upperfirst' : sifter.validators.Tag('UPPERFIRST'),
                    'quotewildcard' : sifter.validators.Tag('QUOTEWILDCARD'),
                    'quoteregex' : sifter.validators.Tag('QUOTEREGEX'),
                    'encodeurl' : sifter.validators.Tag('ENCODEURL'),
                    'length' : sifter.validators.Tag('LENGTH'),
                },
                [ 
                    sifter.validators.StringList(length=1),
                    sifter.validators.StringList(length=1),
                ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)

        self.variable_modifier = tagged_args
        self.variable_name = positional_args[0][0]
        if (not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', self.variable_name)):
            raise sifter.grammar.RuleSyntaxError("Illegal variable name '%s' encountered" % self.variable_name)
        self.variable_value = positional_args[1][0]

    def evaluate(self, message, state):
        state.check_required_extension('variables', 'VARIABLES')
        variable_value = sifter.grammar.string.expand_variables(self.variable_value, state)
        if 'lower' in self.variable_modifier:
            variable_value = variable_value.lower()
        if 'upper' in self.variable_modifier:
            variable_value =  variable_value.upper()
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
            try:
                variable_value = urllib.quote(variable_value, safe='-._~')
            except AttributeError:
                variable_value = urllib.parse.quote(variable_value, safe='-._~')
        if 'length' in self.variable_modifier:
            variable_value = "" + len(variable_value)
        state.named_variables[self.variable_name] = variable_value

CommandSet.register()
