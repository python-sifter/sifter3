import email.utils

import sifter.grammar
import sifter.grammar.string
import sifter.validators

__all__ = ('TestEnvelope',)

# section 5.4
class TestEnvelope(sifter.grammar.Test):

    RULE_IDENTIFIER = 'ENVELOPE'

    def __init__(self, arguments=None, tests=None):
        super(TestEnvelope, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sifter.validators.Comparator(),
                    'match_type' : sifter.validators.MatchType(),
                    'address_part' : sifter.validators.Tag(
                                        ('LOCALPART', 'DOMAIN', 'ALL')),
                },
                [
                    sifter.validators.StringList(),
                    sifter.validators.StringList(),
                ]
            )
        self.validate_tests_size(0)

        self.envelopeparts, self.keylist = positional_args
        self.match_type = self.comparator = self.address_part = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]
        if 'address_part' in tagged_args:
            self.address_part = tagged_args['address_part'][0]

    def evaluate(self, message, state):
        state.check_required_extension('envelope', 'tests against the SMTP envelope')
        envelopeparts = [str.lower(sifter.grammar.string.expand_variables(x, state)) for x in self.envelopeparts]
        for envelopepart in envelopeparts:
            if envelopepart != 'from' and envelopepart != 'to':
                raise sifter.grammar.RuleSyntaxError(
                    "envelope part '%s' is unsupported" % envelopepart)
        envelope_from = message.get_unixfrom()
        envelope_from = envelope_from if envelope_from else ''
        try:
            if envelope_from.startswith('From '):
                # Unix From line 'From envelope_from@domain Date More'
                envelope_from = envelope_from.split(' ')[1]
                addresses = email.utils.getaddresses([envelope_from,])
                _, envelope_from = addresses[0] if len(addresses) > 0 else ''
                envelope_to = ''
            else:
                # we expect '<envelope_from@domain>, <envelope_to@domain>', the latter optional
                addresses = email.utils.getaddresses([envelope_from])
                _, envelope_from = addresses[0] if len(addresses) > 0 else ''
                _, envelope_to = addresses[1] if len(addresses) > 1 else ''
            if envelope_from:
                envelope_from = sifter.grammar.string.address_part(envelope_from, self.address_part)
            if envelope_to:
                envelope_to = sifter.grammar.string.address_part(envelope_from, self.address_part)
        except:
            return False 
        for envelopepart in envelopeparts:
            for key in self.keylist:
                key = sifter.grammar.string.expand_variables(key, state)
                if sifter.grammar.string.compare(
                        envelope_from if envelopepart == 'from' else envelope_to,
                        key, state, self.comparator, self.match_type):
                    return True
        return False

TestEnvelope.register()
