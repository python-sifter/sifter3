import sifter.grammar
import sifter.validators

__all__ = ('CommandRewrite',)

# section 4.1
class CommandRewrite(sifter.grammar.Command):

    RULE_IDENTIFIER = 'REWRITE'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandRewrite, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(length=1),
                  sifter.validators.StringList(length=1),
                ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.search = positional_args[0][0]
        self.replace = positional_args[1][0]

    def evaluate(self, message, state):
        state.check_required_extension('rewrite', 'REWRITE')
        search = sifter.grammar.string.expand_variables(self.search, state)
        replace = sifter.grammar.string.expand_variables(self.replace, state)
        state.actions.append('rewrite', (search, replace))

CommandRewrite.register()
