"""
This program uses PLY (Python Lex-Yacc). Documentation for PLY is
available at
    http://www.dabeaz.com/ply/ply.html

PLY can be installed on your own system using pip, which comes
preinstalled on recent versions of Python (>= 3.4). Using pip the PLY
package can be installed with the following command:
    pip3 install ply
This requires Internet access to download the package.
"""

import ply.lex as lex
import sys

"""
PLY's scanner works by matching regular expressions to the tokens.
Regular expressions were used in the superquiz, but if anyone needs
a reminder of the syntax check the following link:
    https://docs.python.org/3/library/re.html

All tokens that the lexer can find must be decleared in a list of
strings called tokens, which contains the names of the tokens, but
not the regular expressions matching them.
"""

# reserved words
reserved = {
    'do': 'DO',
    'else': 'ELSE',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'while': 'WHILE',
    'read' : 'READ',
    'write': 'WRITE'    
}

# all token types
tokens = [
    'SEM', 'BEC', 'LESS', 'EQ', 'GRTR', 'LEQ', 'NEQ', 'GEQ',
    'ADD', 'SUB', 'MUL', 'DIV', 'LPAR', 'RPAR', 'NUM', 'ID'
] + list(reserved.values())

"""
A regular expression is associated to a token as in the following
example:

    t_EXAMPLE1 = r'\+'

The declared name must start with 't_' and end with the name of a
token (an element of tokens). It is assigned a string denoting a
regular expression. The prefix 'r' of the string is not related to
regular expressions but specifies raw strings in Python. In raw
strings, Python does not treat backslashes as escape sequences.

By declaring a function instead of a string, an action can be
performed after a token has been matched:

    def t_EXAMPLE2(t):
        r'\+'
        t.type = 'ADD' # must be the name of a token
        t.value = 'ADD' # can be any value associated with the token
        return t

In this case, the regular expression is the docstring of the
function. The function has a single input 't', a token object with
attributes type and value, both of which are already set. The
attribute t.type is set to the function's name without 't_' and
t.value is set to the string that the regular expression matched.
These attributes can be modified if necessary, as shown above.
"""

# rules specifying regular expressions and actions

t_SEM = r';'
t_BEC = r':='
t_LESS = r'<'
t_EQ = r'='
t_GRTR = r'>'
t_LEQ = r'<='
t_NEQ  = r'!='
t_GEQ = r'>='
t_ADD = r'\+'
t_SUB = r'-'
t_MUL  = r'\*'
t_DIV  = r'/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_NUM  = r'[0-9]+'


def t_ID(t):
    r'[a-z]+'
    if t.value in reserved:
        t.type = reserved[t.value]  
    else:
        t.type = 'ID'        
    return t

# rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# rule to ignore whitespace
t_ignore = ' \t'

# error handling rule
def t_error(t):
    print("lexical error: illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

# Show all tokens in the input.

scanner = lex.lex()
scanner.input(sys.stdin.read())

for token in scanner:
    if token.type in ['NUM', 'ID']:
        print(token.type, token.value)
    else:
        print(token.type)
