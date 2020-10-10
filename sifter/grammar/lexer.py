# Parser based on RFC 5228, especially the grammar as defined in section 8. All
# references are to sections in RFC 5228 unless stated otherwise.

import re
from typing import (
    Any,
    Optional,
    Text
)

import math
from ply.lex import lex, LexToken  # type: ignore


class SieveLexer():

    def __init__(self, debug: bool = False) -> None:
        self.lexer = lex(
            module=self,
            debug=debug
        )
        self.lexer.linestart = 0

    def __iter__(self) -> Any:
        return iter(self.lexer)

    def token(self) -> Any:
        return self.lexer.token()

    def input(self, data: Text) -> None:
        self.lexer.input(data)

    tokens = (
        'IDENTIFIER', 'NUMBER', 'TAG', 'HASH_COMMENT', 'BRACKET_COMMENT',
        'QUOTED_STRING', 'MULTILINE_STRING',
    )
    literals = [c for c in ';,()[]{}']

    # section 2.2
    t_ignore = ' \t'

    # section 2.3
    def t_HASH_COMMENT(self, t: 'LexToken') -> None:
        r'\#.*\r?\n'
        t.lexer.lineno += 1

    # section 2.3
    def t_BRACKET_COMMENT(self, t: 'LexToken') -> None:
        r'/\*[\r\n\S\s.]*?\*/'
        # Bracketed comments begin with the token "/*" and end with "*/"
        # outside of a string.  Bracketed comments may span multiple lines.
        # Bracketed comments do not nest.

    # section 2.4.2
    def t_MULTILINE_STRING(self, t: 'LexToken') -> Optional['LexToken']:
        r'text:\s?(?:\#.*)\r?\n(?P<multilinetext>[\r\n\S\s.]*?\r?\n)\.\r?\n'
        # For entering larger amounts of text, such as an email message,
        # a multi-line form is allowed.  It starts with the keyword "text:",
        # followed by a CRLF, and ends with the sequence of a CRLF, a single
        # period, and another CRLF.  The CRLF before the final period is
        # considered part of the value.  In order to allow the message to
        # contain lines with a single dot, lines are dot-stuffed.  That is,
        # when composing a message body, an extra '.' is added before each line
        # that begins with a '.'.  When the server interprets the script, these
        # extra dots are removed.  Note that a line that begins with a dot
        # followed by a non-dot character is not interpreted as dot-stuffed;
        # that is, ".foo" is interpreted as ".foo".  However, because this is
        # potentially ambiguous, scripts SHOULD be properly dot-stuffed so such
        # lines do not appear.
        t.value = t.lexer.lexmatch.group('multilinetext')
        t.value = re.sub(r'(\r?\n\.)\.', r'\1', t.value)
        return t

    # section 2.4.2
    def t_QUOTED_STRING(self, t: 'LexToken') -> Optional['LexToken']:
        r'"([^"\\]|\\["\\])*"'
        # TODO: Add support for:
        # - An undefined escape sequence (such as "\a" in a context where "a"
        # has no special meaning) is interpreted as if there were no backslash
        # (in this case, "\a" is just "a"), though that may be changed by
        # extensions.
        # - Non-printing characters such as tabs, CRLF, and control characters
        # are permitted in quoted strings.  Quoted strings MAY span multiple
        # lines.  An unencoded NUL (US-ASCII 0) is not allowed in strings.
        t.value = t.value.strip('"').replace(r'\"', '"').replace(r'\\', '\\')
        return t

    def t_TAG(self, t: 'LexToken') -> Optional['LexToken']:
        r':[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = t.value[1:].upper()
        return t

    def t_IDENTIFIER(self, t: 'LexToken') -> Optional['LexToken']:
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = t.value.upper()
        return t

    # section 2.4.1
    def t_NUMBER(self, t: 'LexToken') -> Optional['LexToken']:
        r'[0-9]+[KkMmGg]?'
        exponents = {
            'G': 30, 'g': 30,
            'M': 20, 'm': 20,
            'K': 10, 'k': 10,
        }
        if t.value[-1] in exponents:
            t.value = math.ldexp(int(t.value[:-1]), exponents[t.value[-1]])
        else:
            t.value = int(t.value)
        return t

    def t_newline(self, t: 'LexToken') -> None:
        r'(\r?\n)+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t: 'LexToken') -> None:
        t.lexer.skip(1)
