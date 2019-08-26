import sifter.handler

__all__ = ('register', 'get_match_fn',)

def register(comparator_name, comparator_cls):
    sifter.handler.register('comparator', comparator_name, comparator_cls)

def get_match_fn(comparator, match_type):
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
    if match_type is None: match_type = 'IS'

    # TODO: support wildcard matching in comparator names (RFC 4790)
    cmp_handler = sifter.handler.get('comparator', comparator)
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

