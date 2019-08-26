import sifter.grammar

__all__ = ('EvaluationState',)

class EvaluationState(object):

    def __init__(self):
        self.actions = sifter.grammar.Actions(implicit_keep=True)
        self.required_extensions = {}
        # section 6.1: the built-in comparators have defined capability
        # strings, but they do not need to be explicitly REQUIRE'd before being
        # used.
        for ext in ('comparator-i;octet', 'comparator-i;ascii-casemap'):
            self.require_extension(ext)
        # variables extension
        self.named_variables = {}
        self.match_variables = []

    def require_extension(self, extension):
        self.required_extensions[extension] = True

    def have_extension(self, extension):
        return extension in self.required_extensions

    def check_required_extension(self, extension, feature_string):
        if extension not in self.required_extensions:
            raise RuntimeError(
                    "REQUIRE '%s' must happen before %s can be used."
                    % (extension, feature_string)
                    )
        return True
