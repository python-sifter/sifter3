import sifter.grammar
import sifter.validators

__all__ = ('CommandPipe',)

class CommandPipe(sifter.grammar.Command):

    RULE_IDENTIFIER = 'PIPE'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandPipe, self).__init__(arguments, tests, block)
        _, positional_args = self.validate_arguments(
                {},
                [ sifter.validators.StringList(length=1), ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)
        self.pipe_dest = positional_args[0]

    def evaluate(self, message, state):
        state.check_required_extension('pipe', 'PIPE')
        pipe_dest = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.pipe_dest)
        state.actions.append('pipe', pipe_dest)
        state.actions.cancel_implicit_keep()

CommandPipe.register()

