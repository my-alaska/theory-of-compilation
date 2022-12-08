#!/usr/bin/python

import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

HAVE_ERRORS = False

lexer = scanner.lexer

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
    p[0] = p[1]

def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = p[1]

def p_instructions_opt_2(p):
    """instructions_opt : """



def p_instructions_1(p):
    """instructions : instructions instruction
                    | instruction """
    if len(p) <= 2:
        p[0] = AST.Instructions(p[1],lineno=lexer.lineno)
    else:
        p[0] = AST.Instructions(p[1],p[2],lineno=lexer.lineno)

def p_instructions_3(p):
    """instruction : '{' instructions '}' """
    p[0] = p[2]




def p_instruction(p):
    """instruction : if
                   | loop
                   | return ';'
                   | assignment ';'
                   | print ';'
                   | breakContinue """
    p[0] = p[1]

def p_breakContinue(p):
    """breakContinue : BREAK ';'
                     | CONTINUE ';' """
    p[0] = AST.BreakContinue(p[1],lineno=lexer.lineno)


def p_if(p):
    """if : IF '(' expression ')' instruction %prec IFX
          | IF '(' expression ')' instruction ELSE instruction """
    if len(p) < 6:
        p[0] = AST.IfOrElse(p[3],p[5],lineno=lexer.lineno)
    else:
        p[0] = AST.IfOrElse(p[3],p[5],p[7],lineno=lexer.lineno)


def p_loop(p):
    """loop : for
            | while"""
    p[0] = p[1]

def p_for(p):
    """for : FOR ID '=' expression ':' expression instruction"""
    p[0] = AST.For(p[2], p[4],p[6], p[7],lineno=lexer.lineno)

def p_while(p):
    """while : WHILE '(' expression ')' instruction"""
    p[0] = AST.While(p[3],p[5],lineno=lexer.lineno)


def p_return(p):
    """return : RETURN
              | RETURN expression"""
    if len(p) > 2:
        p[0] = AST.Return(p[2],lineno=lexer.lineno)
    else:
        p[0] = AST.Return(lineno=lexer.lineno)


def p_assignment(p):
    """assignment : assignable assign_operator expression """
    p[0] = AST.Assign(p[1],p[2],p[3],lineno=lexer.lineno)



def p_assign_operator(p):
    """ assign_operator : '='
                        | ADDASSIGN
                        | SUBASSIGN
                        | MULASSIGN
                        | DIVASSIGN """
    p[0] = p[1]

# def p_assignable(p):
#     """ assignable : id
#                   | id '[' function_args ']' """
#     if len(p) > 2:
#         p[0] = AST.MatrixAccess(p[1],p[3],lineno=lexer.lineno)
#     else : p[0] = p[1]

def p_assignable(p):
    """ assignable : id
                  | id '[' expression ',' expression ']' """
    if len(p) > 2:
        p[0] = AST.MatrixAccess(p[1],p[3],p[5],lineno=lexer.lineno)
    else : p[0] = p[1]

def p_id(p):
    """id : ID"""
    p[0] = AST.Identifier(p[1],lineno=lexer.lineno)

def p_print(p):
    """print : PRINT printable_list"""
    p[0] = AST.Print(p[2],lineno=lexer.lineno)


def p_printable_list(p):
    """printable_list : printable_list ',' printable
                      | printable"""
    if len(p) > 2:
        p[0] = AST.PrintBody(p[1],p[3],lineno=lexer.lineno)
    else:
        p[0] = AST.PrintBody(p[1],lineno=lexer.lineno)




def p_printable(p):
    """printable : string
                 | expression"""
    p[0] = p[1]

def p_string(p):
    """string : STRING"""
    p[0] = AST.String(p[1],lineno=lexer.lineno)

def p_expression(p):
    """expression : int
                  | float
                  | assignable
                  | bracketed

                  | matrix
                  | matrix_function

                  | binary_expr

                  | uminus
                  | transposition
                  """
    p[0] = p[1]

def p_bracketed(p):
    """bracketed : '(' expression ')'"""
    p[0] = p[2]

def p_int(p):
    """int : INTNUM """
    p[0] = AST.IntNum(p[1],lineno=lexer.lineno)

def p_float(p):
    """float : FLOATNUM"""
    p[0] = AST.FloatNum(p[1],lineno=lexer.lineno)

def p_binary_expr(p):
    """ binary_expr : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression

                      | expression DOTADD expression
                      | expression DOTSUB expression
                      | expression DOTMUL expression
                      | expression DOTDIV expression

                      | expression '<' expression
                      | expression '>' expression
                      | expression ELESS expression
                      | expression EGREATER expression
                      | expression EQUALS expression
                      | expression NEQUALS expression """

    p[0] = AST.BinExpr(p[1],p[2],p[3],lineno=lexer.lineno)

def p_uminus(p):
    """uminus : '-' expression %prec UMINUS"""
    p[0] = AST.UnaryMinus(p[2],lineno=lexer.lineno)

def p_transposition(p):
    """transposition : expression "'" """
    p[0] = AST.Transpose(p[1],lineno=lexer.lineno)


def p_matrix(p):
    """matrix : '[' vector_1 ']' """
    p[0] = AST.Matrix(p[2],lineno=lexer.lineno)

def p_vector_1(p):
    """vector_1 : vector_1 ',' '[' vector_2 ']'
                    | '[' vector_2 ']' """
    if len(p) > 4:
        p[0] = AST.MatrixBody(p[1],p[4],lineno=lexer.lineno)
    else: p[0] = AST.MatrixBody(p[2],lineno=lexer.lineno)


def p_vector_2(p):
    """vector_2 : vector_2 ',' expression
                    | expression """
    if len(p) > 2:
        p[0] = AST.Vector(p[1],p[3],lineno=lexer.lineno)
    else: p[0] = AST.Vector(p[1],lineno=lexer.lineno)


# def p_matrix_function(p):
#     """matrix_function :  function_name '(' function_args ')' """
#     p[0] = AST.Function(p[1],p[3],lineno=lexer.lineno)
#
# def p_function_name(p):
#     """function_name : EYE
#                      | ZEROS
#                      | ONES """
#     p[0] = p[1]
#
# def p_function_args(p):
#     """ function_args : function_args ',' expression
#                       | expression"""
#     if len(p) > 2:
#         p[0] = AST.FunctionArgs(p[1],p[3],lineno=lexer.lineno)
#     else: p[0] = AST.FunctionArgs(p[1],lineno=lexer.lineno)

def p_matrix_function(p):
    """matrix_function :  function_name '(' expression ')' """
    p[0] = AST.Function(p[1],p[3],lineno=lexer.lineno)

def p_function_name(p):
    """function_name : EYE
                     | ZEROS
                     | ONES """
    p[0] = p[1]


