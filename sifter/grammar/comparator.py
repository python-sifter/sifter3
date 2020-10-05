from typing import (
    Optional,
    Text,
    Pattern,
    Match
)

import re
from sifter.grammar.sieveobject import SieveObject
from sifter.grammar.state import EvaluationState


# The official definition of comparators is in RFC 4790
class Comparator(SieveObject):

    HANDLER_TYPE = 'comparator'

    @classmethod
    def sort_key(cls, s: Text) -> Text:
        return s

    # draft-ietf-sieve-regex-01: according to section 5, the :regex match type
    # is available to all comparators. furthermore, string normalization (aka
    # sort_key() above) is only applied to the string to be matched against,
    # not to the regular expression string.
    @classmethod
    def cmp_regex(cls, s: Text, pattern: Pattern[Text], state: EvaluationState) -> Optional[Match[Text]]:
        # section 4: must be used as an extension named 'regex'
        state.check_required_extension('regex', ':regex')
        # TODO: cache compiled pattern for more efficient execution across
        # multiple strings and messages
        # TODO: make sure the specified pattern is allowed by the standard
        # (which allows only extended regular expressions from IEEE Standard
        # 1003.2, 1992): 1) disallow python-specific features, along with word
        # boundaries and backreferences, 2) double-check that python supports
        # all ERE features.
        compiled_re = re.compile(pattern)
        m = compiled_re.search(cls.sort_key(s))
        state.match_variables = []
        if m and state.have_extension('variables'):
            # Get the matched ranges from the original string, not the case-corrected one
            for i in range(0, len(m.groups()) + 1):
                state.match_variables.append(s[m.start(i):m.end(i)])
        return m
