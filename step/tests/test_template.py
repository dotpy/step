"""Test suite for the step.Template class"""

import unittest

import step


class TestTemplate(unittest.TestCase):
    """Test case class for step.Template."""

    def test_variable(self):
        tmpl = "Variable: {{var}}"
        values = {"var": 1}
        output = "Variable: 1"
        self.assertEqual(step.Template(tmpl).expand(values), output)

    def test_escape(self):
        tmpl = "Variable: {\{var}\}"
        output = "Variable: {{var}}"
        self.assertEqual(step.Template(tmpl).expand({}), output)

    def test_condition(self):
        tmpl = r"""I have
               %if eggs == 1:
                  1 egg
               %else:
                  {{eggs}} eggs
               %endif"""
        values = {"eggs": 3}
        output = "I have\n3 eggs"
        self.assertEqual(step.Template(tmpl).expand(values), output)

    def test_isdef(self):
        tmpl = r"""
               %if isdef("spam"):
                   I like spam
               %else:
                   I don't like spam
               %endif"""
        output = "I don't like spam"
        self.assertEqual(step.Template(tmpl).expand({}), output)

    def test_echo(self):
        tmpl = r"""
               <%if eggs == 1:
                   echo("I have 1 egg")
               %>"""
        values = {"eggs": 1}
        output = "I have 1 egg"
        self.assertEqual(step.Template(tmpl).expand(values), output)


    def test_strip(self):
        tmpl = "\n\nName:\t\t\t{{var}}\n \t\n"
        values = {"var": 1}
        output = "Name:\t1"
        self.assertEqual(step.Template(tmpl).expand(values), output)


    def test_double_quote_escape(self):
        tmpl = r'abc""defg"""hijk""""lmn"""""'
        self.assertEqual(step.Template(tmpl).expand(), tmpl)


    def test_backslash_escape(self):
        tmpl_list = [
            r'===\n===',
            r'===\f===',
            r'===\\===',
            '===\n===',
            '===\f===',
            '===\\===',
            '===\\n===',
            '===\\\n===',
            '===\\\\n===',
        ]
        for tmpl in tmpl_list:
            self.assertEqual(step.Template(tmpl).expand(), tmpl)

