#!/usr/bin/python

import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

HAVE_ERRORS = False

precedence = (

    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),

    ('left', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',),
    ("nonassoc", '<', '>', 'ELESS', 'EGREATER', 'EQUALS', 'NEQUALS'),

    ("left", '+', '-'),
    ("left", '*', '/'),

    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),

    ("left", "'"),
    ("right", "UMINUS"),



)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""

def p_instructions_opt_1(p):
    """instructions_opt : instructions """

def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction
                    | instruction """

def p_instructions_3(p):
    """instruction : '{' instructions '}' """



def p_instruction(p):
    """instruction : if
                   | loop
                   | return ';'
                   | assignment ';'
                   | print ';'
                   | BREAK ';'
                   | CONTINUE ';' """


def p_if(p):
    """if : IF '(' expression ')' instruction %prec IFX
          | IF '(' expression ')' instruction ELSE instruction """


def p_loop(p):
    """loop : FOR ID '=' expression ':' expression instruction
            | WHILE '(' expression ')' instruction"""


def p_return(p):
    """return : RETURN
              | RETURN expression"""


def p_assignment(p):
    """assignment : assignable '=' expression
                  | assignable ADDASSIGN expression
                  | assignable SUBASSIGN expression
                  | assignable MULASSIGN expression
                  | assignable DIVASSIGN expression"""

def p_assignable(p):
    """assignable : ID
                  | ID '[' expression ',' expression ']' """


def p_print(p):
    """print : PRINT printable_list"""


def p_printable_list(p):
    """printable_list : printable_list ',' printable
                      | printable"""

def p_printable(p):
    """printable : STRING
                 | expression"""


def p_expression(p):
    """expression : assignable
                  | '(' expression ')'
                  | INTNUM
                  | FLOATNUM

                  | matrix
                  | matrix_function '(' expression ')'

                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | '-' expression %prec UMINUS

                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression

                  | expression '<' expression
                  | expression '>' expression
                  | expression ELESS expression
                  | expression EGREATER expression
                  | expression EQUALS expression
                  | expression NEQUALS expression
                  | expression "'"
                  """

def p_matrix(p):
    """matrix : '[' vector_1 ']' """
def p_vector_1(p):
    """vector_1 : vector_1 ',' '[' vector_2 ']'
                    | '[' vector_2 ']' """
def p_vector_2(p):
    """vector_2 : vector_2 ',' expression
                    | expression """


def p_matrix_function(p):
    """matrix_function : EYE
                       | ZEROS
                       | ONES"""

# parser = yacc.yacc( )

