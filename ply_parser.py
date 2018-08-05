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
import ply.yacc as yacc
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
t_NUM  = r'd+'

### add code for inequality, multiplication, division and numbers ###

def t_ID(t):
    r'[a-z]+'
    if t.value in reserved:
        t.type = reserved[t.value]  
    else:
        t.type = 'ID'        
    ### add code for reserved words using the dictionary above ###
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

def indent(s, level):
    return '    '*level + s + '\n'

# Each of the following classes is a kind of node in the abstract syntax tree.
# indented(level) returns a string that shows the tree levels by indentation.

class Program_AST:
    def __init__(self, program):
        self.program = program
    def __repr__(self):
        return repr(self.program)
    def indented(self, level):
        return self.program.indented(level)

class Statements_AST:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result
    def indented(self, level):
        result = indent('Statements', level)
        for st in self.statements:
            result += st.indented(level+1)
        return result
    
class If_Else_AST:
    def __init__(self, condition, then, again):
        self.condition = condition
        self.then = then
        self.again = again
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
                       repr(self.then) + ' else ' + \
                       repr(self.again) + 'end'
    def indented(self, level):
        return indent('If-Else', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1) + \
               self.again.indented(level+1)

class If_AST:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
                       repr(self.then) + ' end'
    def indented(self, level):
        return indent('If', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1)

class While_AST:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return 'while ' + repr(self.condition) + ' do ' + \
                          repr(self.body) + ' end'
    def indented(self, level):
        return indent('While', level) + \
               self.condition.indented(level+1) + \
               self.body.indented(level+1)

class Assign_AST:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return repr(self.identifier) + ':=' + repr(self.expression)
    def indented(self, level):
        return indent('Assign', level) + \
               self.identifier.indented(level+1) + \
               self.expression.indented(level+1)

class Write_AST:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return 'write ' + repr(self.expression)
    def indented(self, level):
        return indent('Write', level) + self.expression.indented(level+1)

class Read_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return 'read ' + repr(self.identifier)
    def indented(self, level):
        return indent('Read', level) + self.identifier.indented(level+1)

class Comparison_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return repr(self.left) + self.op + repr(self.right)
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)

class Expression_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return '(' + repr(self.left) + self.op + repr(self.right) + ')'
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)

class Number_AST:
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return self.number
    def indented(self, level):
        return indent(self.number, level)

class Identifier_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return self.identifier
    def indented(self, level):
        return indent(self.identifier, level)

# --------------------------------------------------------------------
#  Parser - Productions defined using the yacc library of PLY
# --------------------------------------------------------------------
"""
PLYs grammars are written in BNF. Each rule has a non-terminal on the
left-hand side and can have a mixture of non-terminals and terminals on
the right-hand side. Terminals are the tokens produced by the scanner.

PLY allows an action to be performed after a rule is reduced, as in
the following example:

    def p_rule_name(p):
        'A : B C D'
        p[0] = p[1] + p[2] + p[3]

The function's name must start with 'p_'. The BNF rule is the docstring
of the function. Separate the items of the BNF rule including the colon
by a space.

The parameter p of the function is a list containing the values of a
synthesised attribute for each item in the BNF rule. In the above
example, the attribute value of A is p[0], that of B is p[1], and so on.
When the function is called, p[1:] will have values for the attribute
of each item on the right-hand side of the BNF rule. The function must
set p[0] to the attribute value of the left-hand side non-terminal.
Values in p[1:] are determined by the parser if the corresponding item
is a non-terminal, and are set to t.value from the scanner if the item
is a terminal token t.
"""

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV')
)

def p_program(p):
    'Program : Statements'
    p[0] = Program_AST(p[1])

def p_statements_statement(p):
    'Statements : Statement'
    p[0] = Statements_AST([p[1]])

def p_statements_statements(p):
    'Statements : Statements SEM Statement'
    sts = p[1].statements
    sts.append(p[3])
    p[0] = Statements_AST(sts)

def p_statement(p):
    '''Statement : If
                 | While
                 | Assignment'''
    p[0] = p[1]

def p_if(p):
    'If : IF Comparison THEN Statements END'
    p[0] = If_AST(p[2], p[4])

def p_while(p):
    'While : WHILE Comparison DO Statements END'
    p[0] = While_AST(p[2], p[4])
    
def p_read(p):
    'Read : READ id'
    p[0] = Read_AST(p[2])

def p_write(p):
    'Write : WRITE Exp'
    p[0] = Write_AST(p[2])


def p_assignment(p):
    'Assignment : Id BEC Expression'
    p[0] = Assign_AST(p[1], p[3])

def p_comparison(p):
    'Comparison : Expression Relation Expression'
    p[0] = Comparison_AST(p[1], p[2], p[3])

def p_relation(p):
    '''Relation : EQ
                | NEQ
                | LESS
                | LEQ
                | GRTR
                | GEQ'''
    p[0] = p[1]

def p_expression_binary(p):
    '''Expression : Expression ADD Expression
                  | Expression SUB Expression
                  | Expression MUL Expression
                  | Expression DIV Expression'''
    p[0] = Expression_AST(p[1], p[2], p[3])

def p_expression_parenthesis(p):
    'Expression : LPAR Expression RPAR'
    p[0] = p[2]

def p_expression_num(p):
    'Expression : NUM'
    p[0] = Number_AST(p[1])

def p_expression_id(p):
    'Expression : Id'
    p[0] = p[1]

def p_id(p):
    'Id : ID'
    p[0] = Identifier_AST(p[1])

def p_error(p):
    print("syntax error")
    sys.exit()

scanner = lex.lex()

# Uncomment the following to test the scanner without the parser.
# Show all tokens in the input.
#
# scanner.input(sys.stdin.read())
#
# for token in scanner:
#     if token.type in ['NUM', 'ID']:
#         print(token.type, token.value)
#     else:
#         print(token.type)
# sys.exit()

# Call the parser.

parser = yacc.yacc()
ast = parser.parse(sys.stdin.read(), lexer=scanner)

# Show the syntax tree with levels indicated by indentation.

print(ast.indented(0), end='')