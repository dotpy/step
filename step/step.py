"""A light and fast template engine."""

import re


class Template(object):
    """ """

    def __init__(self, template):
        """Initialize class"""
        super(Template, self).__init__()
        self.template = template
        self.options = {"strip": True}

    def expand(self, namespace={}, **kw):
        """Return the expanded template string"""
        namespace.update(kw)
        output = []

        # Builtins
        namespace["echo"]   = lambda s: output.append(s)
        namespace["isdef"]  = lambda v: v in namespace
        namespace["setopt"] = lambda k, v: self.options.update({k: v})

        code = self._process(self._preprocess(self.template))
        eval(compile(code, "<string>", "exec"), namespace)
        return self._postprocess("".join(map(str, output)))

    def _preprocess(self, template):
        """Modify template string before code conversion"""
        # Replace inline ('%') blocks for easier parsing
        o = re.compile("(?m)^[ \t]*%((if|for|while|try).+:)")
        c = re.compile("(?m)^[ \t]*%(((else|elif|except|finally).*:)|(end\w+))")
        template = c.sub(r"<%:\g<1>%>", o.sub(r"<%\g<1>%>", template))

        # Replace (${x}) variables with '<%echo(x)%>'
        v = re.compile("\${([a-zA-Z0-9[\].\"\'_]+)}")
        template = v.sub(r"<%echo(\g<1>)%>\n", template)

        return template

    def _process(self, template):
        """Return the code generated from the template string"""
        code_blk = re.compile(r"<%(.*?)%>\n?", re.DOTALL)
        indent = 0
        code = []
        for n, blk in enumerate(code_blk.split(template)):
            # Replace '<\%' and '%\>' escapes
            blk = re.sub(r"<\\%", "<%", re.sub(r"%\\>", "%>", blk))
            # Unescape '%{}' characters
            blk = re.sub(r"\\(%|{|})", "\g<1>", blk)

            if not (n % 2):
                # Escape double-quote characters
                blk = re.sub(r"\"", "\\\"", blk)
                blk = (" " * (indent*4)) + 'echo("""{}""")'.format(blk)
            else:
                blk = blk.rstrip()
                if blk.lstrip().startswith(":"):
                    if not indent:
                        err = "unexpected block ending"
                        raise SyntaxError("Line {}: {}".format(n, err))
                    indent -= 1
                    if blk.startswith(":end"):
                        continue
                    blk = blk.lstrip()[1:]

                blk = re.sub("(?m)^", " " * (indent * 4), blk)
                if blk.endswith(":"):
                    indent += 1

            code.append(blk)

        if indent:
            err = "Reached EOF before closing block"
            raise EOFError("Line {}: {}".format(n, err))

        return "\n".join(code)

    def _postprocess(self, output):
        """Modify output string after variables and code evaluation"""
        if self.options["strip"]:
            output = re.sub("(?m)(^[ \t]+|[ \t]+$|(?<=[ \t])[ \t]+|^\n)", "",
                            output)

        return output
