import re
from typing import (
    TYPE_CHECKING,
    Text,
    Optional,
    Union
)
import sifter.comparator
from sifter.grammar.state import EvaluationState

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag

# Grammar for string variable expansion, RFC 5229, section 3
_variable_re_identifier = r'(?:[A-Za-z_][A-Za-z0-9_]*)'
_variable_re_num_variable = r'(?:[0-9]+)'
_variable_re_variable_name = r'(?:' + _variable_re_num_variable + r'|' + _variable_re_identifier + r')'
_variable_re_sub_namespace = r'(?:' + _variable_re_variable_name + r'\.)'
_variable_re_namespace = r'(?:' + _variable_re_identifier + r'\.(?:' + _variable_re_sub_namespace + r'*))'
_variable_re_variable_ref = r'\$\{(' + _variable_re_namespace + r')?(' + _variable_re_variable_name + r')\}'
_variable_re = re.compile(_variable_re_variable_ref)


# TODO: this is here because it'll be needed when support for encoded
# characters and variables is added. for now it's just a wrapper around str.
class String(str):
    pass


def expand_variables(s: Text, state: EvaluationState) -> Text:
    if s and state.have_extension('variables'):
        for m in reversed(list(_variable_re.finditer(s))):
            if m.group(1):
                raise RuntimeError("Variable namespaces not supported")
            try:
                if m.group(2).isdigit():
                    r = state.match_variables[int(m.group(2))]
                else:
                    r = state.named_variables[m.group(2)]
            except Exception:
                r = ''
            s = s[:m.start()] + r + s[m.end():]
    return s


def compare(
    str1: Text,
    str2: Text,
    state: EvaluationState,
    comparator: Optional[Union[Text, 'Tag']] = None,
    match_type: Optional[Union[Text, 'Tag']] = None
) -> bool:
    cmp_fn, comparator, match_type = sifter.comparator.get_match_fn(comparator, match_type)
    state.check_required_extension('comparator-%s' % comparator, 'the comparator')
    return cmp_fn(str1, str2, state)


def address_part(address: Text, part: Optional[Text] = None) -> Text:
    # section 2.7.4: default address part is ":all"
    if part is None:
        part = 'ALL'

    if part == 'ALL':
        return address
    try:
        localpart, domain = address.rsplit('@', 1)
    except ValueError:
        # if there's no '@' in the address then treat the whole address as the
        # local part
        localpart = address
        domain = ''
    if part == 'LOCALPART':
        return localpart
    if part == 'DOMAIN':
        return domain
    raise RuntimeError("Unknown address part specified: %s" % part)
