from typing import (
    TYPE_CHECKING,
    Callable,
    Text,
    Optional,
    Tuple,
    Union
)

from sifter.extensions import ExtensionRegistry

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag
    from sifter.grammar.state import EvaluationState


def get_match_fn(
    comparator: Optional[Union[Text, 'Tag']],
    match_type: Optional[Union[Text, 'Tag']]
) -> Tuple[Callable[[Text, Text, 'EvaluationState'], bool], Union[Text, 'Tag'], Union[Text, 'Tag']]:
    # section 2.7.3: default comparator is 'i;ascii-casemap'
    # RFC 4790, section 3.1: the special identifier 'default' refers to the
    # implementation-defined default comparator
    if comparator is None or comparator == 'default':
        if match_type != 'REGEX':
            comparator = 'i;ascii-casemap'
        else:
            # 'i;ascii-casemap' uppercases test string but not pattern, which
            # is is very counter intuitive -> change default for regex
            comparator = 'i;octet'

    # section 2.7.1: default match type is ":is"
    if match_type is None:
        match_type = 'IS'

    # TODO: support wildcard matching in comparator names (RFC 4790)
    cmp_handler = ExtensionRegistry.get_comparator(comparator)
    if not cmp_handler:
        raise RuntimeError("Comparator not supported: %s" % comparator)

    try:
        cmp_fn = getattr(cmp_handler, 'cmp_%s' % match_type.lower())
    except AttributeError:
        raise RuntimeError(
            "':%s' matching not supported by comparator '%s'"
            % (match_type, comparator)
        )

    return (cmp_fn, comparator, match_type)
