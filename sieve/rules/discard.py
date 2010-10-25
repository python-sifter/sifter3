import base

# section 4.4
class SieveCommandDiscard(base.SieveCommand):

    RULE_IDENTIFIER = 'DISCARD'

    def __init__(self, arguments=None, tests=None, block=None):
        base.SieveCommand.__init__(self, arguments, tests, block)
        self.validate_arguments_size(0)
        self.validate_tests_size(0)
        self.validate_block_size(0)

    def evaluate(self, message, state):
        state['actions'].cancel_implicit_keep()
