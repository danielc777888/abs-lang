from distutils.core import setup

setup(name = "ply",
            description="Python Lex & Yacc",
            long_description = """PLY is yet another implementation of lex and yacc for Python. Although several o
ther parsing tools are available for Python, there are several reasons why you m
ight want to take a look at PLY: 

It's implemented entirely in Python. 

It uses LR-parsing which is reasonably efficient and well suited for larger gram
mars. 

PLY provides most of the standard lex/yacc features including support for empty 
productions, precedence rules, error recovery, and support for ambiguous grammar
s. 

PLY is extremely easy to use and provides very extensive error checking. 
""",
            licence="""Lesser GPL (LGPL)""",
            version = "1.3.1",
            author = "David Beazley",
            author_email = "beazley@cs.uchicago.edu",
            maintainer = "David Beazley",
            maintainer_email = "beazley@cs.uchicago.edu ",
            url = "http://systems.cs.uchicago.edu/ply/",
            py_modules = ["lex","yacc"],
            )
