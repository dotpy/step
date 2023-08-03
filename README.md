step - Simple Template Engine for Python
========================================


`step` is a pure-Python module providing a very simple template engine with
minimum syntax. It supports variable expansion, flow control and embedding of
Python code.


Installation
------------
Use pip:

    # pip install step-template

or download the package from [GitHub](https://github.com/dotpy/step/) and run the
install script:

    # python setup.py install


Basic usage
-----------
A template is a string containing any kind of textual content and a set of
directives representing variables, control structures and blocks of Python code.

Variables are enclosed in `{{}}` and follow the same syntax rules as Python
variables; e.g.:

    This is variable x: {{x}}
    This is the third item of my_list: {{my_list[2]}}
    This is not a variable: \{\{x\}\}

If `Template` is created with `escape=True`, all variables are auto-escaped
for HTML, unless given with a leading exclamation mark; e.g. `raw x: {{!x}}`.
The escape-function can be changed via `Template().builtins`.

Flow control expressions are written like regular Python control structures,
preceded by the `%` sign and must be closed by a `%end<statement>` tag; e.g.:

    %if (x > 2):
        x is greater than 2
    %else:
        x is {{x}}
    %endif

All text between `<%` and `%>` is considered Python code; you can use the
builtin `echo()` function to output some text from within Python code blocks;
e.g.:

    <%
    import time
    echo("Current timestamp is {}".format(time.time()))
    %>
    <\% This is not Python code %\>

You can use the special function `isdef()` to perform some actions only if a
name is defined in the template namespace; e.g.:

    %if isdef("my_var")
        my_var is {{my_var}}
    %endif

The `get()` function returns the specified value from template namespace,
or given fallback if name is undefined, defaulting to `None`; e.g.:

    {{get("x")}} {{get("y", 2)}}

The `setopt()` function allows you to enable options that modify the template
output; the only supported option is 'strip', which removes leading/trailing
whitespace, contiguous whitespace and empty lines and defaults to true; e.g.:

    <%setopt("strip", True)%>

The 'strip' option can also be given as a parameter during `Template` object
creation; e.g.:

    tmpl = step.Template(TEMPLATE_STRING, strip=True)

A backslash at the end of a line will suppress the newline character.


Documentation
-------------
More examples and a detailed description of the module and its classes are
available at http://www.kernel-panic.it/programming/step/.


Tests
-----
To run the test suite, just run `python setup.py test`.


Credits
-------
Copyright (c) 2012 Daniele Mazzocchio (danix@kernel-panic.it).
Several improvements by Erki Suurjaak.

Licensed under the BSD license (see [LICENSE.md](LICENSE.md) file).
