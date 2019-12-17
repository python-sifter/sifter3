import sifter.extensions.builtin
import sifter.extensions.regex
from sifter.grammar import grammar
from sifter.grammar import lexer
import logging
import ply.yacc

__all__ = ('parse_file',)

def parse_file(filehandle, tracking=0):
    log = logging.getLogger("sifter")
    yacc = grammar.parser(errorlog=log)
    yacc.errok()
    rules = yacc.parse(filehandle.read(), lexer=lexer.lexer(), tracking=tracking)
    if not yacc.errorok:
        raise ply.yacc.YaccError('Syntax error')
    return rules
    