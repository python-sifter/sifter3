import re

import sifter.grammar

__all__ = ('ComparatorOctet',)

class ComparatorOctet(sifter.grammar.Comparator):

    COMPARATOR_ID = 'i;octet'

    @classmethod
    def cmp_is(cls, str1, str2, state):
        return cls.sort_key(str1) == cls.sort_key(str2)

    @classmethod
    def cmp_contains(cls, s, substring, state):
        return cls.sort_key(substring) in cls.sort_key(s)

    @classmethod
    def cmp_matches(cls, s, pattern, state):
        pattern = cls.sort_key(pattern)
        i, g, n = 0, 0, len(pattern)
        re_pattern = []
        while i < n:
            c = pattern[i]
            i += 1
            if c == "*":
                re_pattern.append("(.*?)")
                g += 1
            elif c == "?":
                re_pattern.append("(.)")
                g += 1
            elif c == "\\":
                if pattern[i:i+1] in ("\\*", "\\?"):
                    re_pattern.append(re.escape(pattern[i+1]))
                    i += 2
                else:
                    re_pattern.append(re.escape(c))
            else:
                re_pattern.append(re.escape(c))
        re_pattern.append("\Z")
        # TODO: compile and cache pattern for more efficient execution across
        # multiple strings and messages
        m = re.match(''.join(re_pattern), cls.sort_key(s),
                re.MULTILINE | re.DOTALL)
        state.match_variables = []
        if m and state.have_extension('variables'):
            # Get the matched ranges from the original string, not the case-corrected one
            for i in range(0, g + 1):
                state.match_variables.append(s[m.start(i):m.end(i)])
        return m

ComparatorOctet.register()
