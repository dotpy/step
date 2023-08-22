"""Test suite for the step.Template class"""

import base64
import io
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
        tmpl = r"Variable: {\{var}\}"
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

    def test_get(self):
        tmpl = r"""{{get("x")}} by {{get("y", 4)}}"""
        output = "2 by 4"
        self.assertEqual(step.Template(tmpl).expand({"x": 2}), output)

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


    def test_postprocess(self):
        tmpl = "something"
        output = tmpl.encode()
        self.assertEqual(step.Template(tmpl, postprocess=str.encode).expand({}), output)
        output = base64.b64encode(tmpl.encode())
        postprocess = (str.encode, base64.b64encode)
        self.assertEqual(step.Template(tmpl, postprocess=postprocess).expand({}), output)


    def test_stream(self):
        tmpl = "something"
        bstream = io.BytesIO()
        step.Template(tmpl).stream(bstream)
        self.assertEqual(bstream.getvalue(), tmpl.encode())
        sstream = io.StringIO()
        step.Template(tmpl).stream(sstream, encoding=None)
        self.assertEqual(sstream.getvalue(), tmpl)


    def test_stream_buffer(self):
        tmpl = r"""
               %for x in iterable:
                   {{x}}
               %endfor
               """
        class writer(list): write = list.append
        vals = [0, 1, 2, 3]
        stream = writer()
        step.Template(tmpl).stream(stream, encoding=None, buffer_size=1, iterable=vals)
        self.assertEqual(stream, ["%s\n" % v for v in vals])
        stream = writer()
        step.Template(tmpl).stream(stream, encoding=None, iterable=vals)
        self.assertEqual(stream, ["\n".join(map(str, vals))])


    def test_autoescape(self):
        HTML = """<a href=""> &' </a>"""
        ESCAPED = """&lt;a href=&quot;&quot;&gt; &amp;&#39; &lt;/a&gt;"""
        tmpl = """{{!%r}} {{%r}}""" % (HTML, HTML)
        for escape in (True, False):
            output = "%s %s" % (HTML, ESCAPED if escape else HTML)
            self.assertEqual(step.Template(tmpl, escape=escape).expand({}), output)


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

