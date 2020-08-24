import email
import os.path
import unittest

import sifter.parser

class TestEvaluateRules(unittest.TestCase):

    EVAL_RESULTS = (
            ("evaluation_1.msg", "evaluation_1.rules",
             [('redirect', 'Coyote@example.com')]),
            ("evaluation_1.msg", "evaluation_2.rules",
             [('fileinto', ['desert'])]),
            ("evaluation_1.msg", "evaluation_3.rules",
             [('notify', ('mailto:shop@example.com', None, None, [], 'birdstuff')),
              ('redirect', 'birdseed@example.com')]),
            ("evaluation_2.msg", "evaluation_1.rules",
             [('redirect', 'postmaster@example.com')]),
            ("evaluation_2.msg", "evaluation_2.rules",
             []),
            ("evaluation_2.msg", "evaluation_3.rules",
             [('pipe', ['cat >> mails.log']),
              ('redirect', 'cash@example.com')]),
    )

    def setUp(self):
        self.messages = {}
        self.rules = {}
        for result in self.EVAL_RESULTS:
            msg_fh = open(os.path.join(os.path.dirname(__file__), result[0]))
            self.messages.setdefault(result[0], email.message_from_file(msg_fh))
            msg_fh.close()
            rule_fh = open(os.path.join(os.path.dirname(__file__), result[1]))
            self.rules.setdefault(result[1], sifter.parser.parse_file(rule_fh))
            rule_fh.close()

    def test_msg_rule_cross_product(self):
        def to_list(obj):
            if obj is None or isinstance(obj, (str, int)):
                return obj
            elif isinstance(obj, (tuple)):
                return tuple(to_list(item) for item in obj)
            else:
                return list(obj)

        for result in self.EVAL_RESULTS:
            self.assertEqual(
                [(action, to_list(value)) for action, value in self.rules[result[1]].evaluate(self.messages[result[0]])],
                result[2]
                )

if __name__ == '__main__':
    unittest.main()
