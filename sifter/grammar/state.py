from typing import (
    Any,
    Text,
    List,
    Dict,
    Optional
)
from sifter.grammar.actions import Actions


class EvaluationState(object):

    def __init__(self) -> None:
        self.actions = Actions(implicit_keep=True)
        self.required_extensions: Dict[Text, bool] = {}
        self.last_if: Optional[bool] = None
        # section 6.1: the built-in comparators have defined capability
        # strings, but they do not need to be explicitly REQUIRE'd before being
        # used.
        for ext in ('comparator-i;octet', 'comparator-i;ascii-casemap'):
            self.require_extension(ext)
        # variables extension
        self.named_variables: Dict[Text, Any] = {}
        self.match_variables: List[Any] = []

    def require_extension(self, extension: Text) -> None:
        self.required_extensions[extension] = True

    def have_extension(self, extension: Text) -> bool:
        return extension in self.required_extensions

    def check_required_extension(self, extension: Text, feature_string: Text) -> bool:
        if extension not in self.required_extensions:
            raise RuntimeError(
                "REQUIRE '%s' must happen before %s can be used."
                % (extension, feature_string)
            )
        return True
