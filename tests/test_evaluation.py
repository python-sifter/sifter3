# type: ignore

import email
import os.path

import sifter.parser


def eval_rules(filename_message, filename_rules):
    with open(os.path.join(os.path.dirname(__file__), filename_message), encoding='utf-8') as msg_fh:
        message = email.message_from_file(msg_fh)
    with open(os.path.join(os.path.dirname(__file__), filename_rules), encoding='utf-8') as rule_fh:
        rules = sifter.parser.parse_file(rule_fh)
    return rules.evaluate(message)


def test_evaulation():

    EVAL_RESULTS = (
        ("evaluation_1.msg", "evaluation_1.rules", [('redirect', 'acm@example.com')]),
        ("evaluation_1.msg", "evaluation_2.rules", []),
        ("evaluation_2.msg", "evaluation_1.rules", [('redirect', 'postmaster@example.com')]),
        ("evaluation_2.msg", "evaluation_2.rules", []),
        ("evaluation_3.msg", "evaluation_1.rules", [('redirect', 'field@example.com')]),
        ("evaluation_3.msg", "evaluation_2.rules", [('fileinto', ['INBOX'])]),
        ("evaluation_3.msg", "evaluation_3.rules", [('keep', None)]),
        ("evaluation_1.msg", "evaluation_4.rules", [('reject', 'I do not accept messages from this address.')]),
        ("evaluation_1.msg", "evaluation_5.rules", [('reject', 'I do not accept messages from\nthis address.\n.\n')]),
        ("evaluation_1.msg", "evaluation_6.rules", [('reject', 'I do not accept messages from this address.')]),
        ("evaluation_1.msg", "evaluation_7.rules", [('reject', 'I do not accept messages from/* this is\nnot a comment */this address.\n.\n')]),
        ("evaluation_1.msg", "evaluation_ihave_reject.rules", [('reject', 'I do not accept messages from this address.')]),
    )

    for messagefile, rulefile, evaluated_rules in EVAL_RESULTS:
        assert evaluated_rules == eval_rules(messagefile, rulefile)
