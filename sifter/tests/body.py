import sifter.grammar
import sifter.grammar.string
import sifter.validators
import re

__all__ = ('TestBody',)

# RFC 5173
class TestBody(sifter.grammar.Test):

    RULE_IDENTIFIER = 'BODY'

    def __init__(self, arguments=None, tests=None):
        super(TestBody, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sifter.validators.Comparator(),
                    'match_type' : sifter.validators.MatchType(),
                    'body_transform' : sifter.validators.BodyTransform(),
                },
                [
                    sifter.validators.StringList(),
                ]
            )
        self.validate_tests_size(0)

        self.keylist = positional_args[0]
        self.body_transform = self.match_type = self.comparator = None
        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]
        if 'body_transform' in tagged_args:
            body_transform_type = tagged_args['body_transform'][0]
            if body_transform_type == 'RAW':
                self.body_transform = []
            elif body_transform_type == 'TEXT':
                self.body_transform = ['text']
            else:
                self.body_transform = tagged_args['body_transform'][1]
        else:
            self.body_transform = ['text']

    def evaluate(self, message, state):
        state.check_required_extension('body', 'tests against the email body')
        if not self.body_transform: # RAW
            # Flatten message, match header / body separator (two new-lines);
            #     if there are no headers, we match ^\n, which is guaranteed to be there
            (_, bodystr) = re.split(r'^\r?\n|\r?\n\r?\n', message.as_string(False), 1)
            return self.evaluate_part(bodystr, state)
        else:
            for msgpart in message.walk():
                if msgpart.is_multipart():
                    # TODO: If "multipart/*" extract prologue and epilogue and make that searcheable
                    # TODO: If "message/rfc822" extract headers and make that searchable
                    # Insetad we skip multipart objects and descend into its children
                    continue
                msgtxt = msgpart.get_payload()
                for mimetype in self.body_transform:
                    if not mimetype: # empty body_transform matches all 
                        if self.evaluate_part(msgtxt, state):
                            return True
                    match = re.match(r'^([^/]+)(?:/([^/]+))?$', mimetype)
                    if not match:
                        continue # malformed body_transform is skipped
                    (maintype, subtype) = match.groups()
                    if maintype == msgpart.get_content_maintype() and (
                            not subtype or subtype == msgpart.get_content_subtype()):
                        if self.evaluate_part(msgtxt, state):
                            return True
        return False

    def evaluate_part(self, part_str, state):
        for key in self.keylist:
            key = sifter.grammar.string.expand_variables(key, state)
            if sifter.grammar.string.compare(part_str, key, state, 
                                             self.comparator, self.match_type):
                return True
        return False

TestBody.register()
