class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)




class Instructions(Node):
    def __init__(self, instr, next_instr=None, lineno = None):
        self.instr = instr
        self.next_instr = next_instr
        self.lineno = lineno




class IntNum(Node):
    def __init__(self, value, lineno = None):
        self.value = value
        self.lineno = lineno

class FloatNum(Node):

    def __init__(self, value, lineno = None):
        self.value = value
        self.lineno = lineno

class String(Node):
    def __init__(self, value, lineno = None):
        self.value = value
        self.lineno = lineno




class Identifier(Node):
    def __init__(self, name, lineno = None):
        self.name = name
        self.lineno = lineno

class BinExpr(Node):
    def __init__(self, left, op, right, lineno = None):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno




# class Function(Node):
#     def __init__(self, name, args, lineno = None):
#         self.name = name
#         self.args = args
#         self.lineno = lineno
#
# class FunctionArgs(Node):
#     def __init__(self, args, lastarg=None, lineno = None):
#         self.args = args
#         self.lastarg = lastarg
#         self.lineno = lineno

class Function(Node):
    def __init__(self, name, arg, lineno = None):
        self.name = name
        self.arg = arg
        self.lineno = lineno






class Print(Node):
    def __init__(self, print_body, lineno = None):
        self.print_body = print_body
        self.lineno = lineno

class PrintBody(Node):
    def __init__(self, args, lastarg=None, lineno = None):
        self.args = args
        self.lastarg = lastarg
        self.lineno = lineno




class For(Node):
    def __init__(self, id, expr1, expr2, instr, lineno = None):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2
        self.instr = instr
        self.lineno = lineno

class While(Node):
    def __init__(self, expr, instr, lineno = None):
        self.expr = expr
        self.instr = instr
        self.lineno = lineno

class IfOrElse(Node):
    def __init__(self, expr, instr1, instr2=None, lineno = None):
        self.expr = expr
        self.instr1 = instr1
        self.instr2 = instr2
        self.lineno = lineno




class Assign(Node):
    def __init__(self, left, assignment, val, lineno = None):
        self.left = left
        self.assignment = assignment
        self.val = val
        self.lineno = lineno




class Matrix(Node):
    def __init__(self, body=None, lineno = None):
        self.body = body
        self.lineno = lineno

class MatrixBody(Node):
    def __init__(self, vecs, lastvec=None, lineno = None):
        self.vecs = vecs
        self.lastvec = lastvec
        self.lineno = lineno

class Vector(Node):
    def __init__(self, items, next_item=None, lineno = None):
        self.items = items
        self.next_item = next_item
        self.lineno = lineno

class MatrixAccess(Node):
    def __init__(self, name, arg1, arg2, lineno = None):
        self.name = name
        self.arg1 = arg1
        self.arg2 = arg2
        self.lineno = lineno




class Transpose(Node):
    def __init__(self, arg, lineno = None):
        self.arg = arg
        self.lineno = lineno

class UnaryMinus(Node):
    def __init__(self, arg, lineno = None):
        self.arg = arg
        self.lineno = lineno

class Return(Node):
    def __init__(self, instr=None, lineno = None):
        self.instr = instr
        self.lineno = lineno

class Break(Node):
    def __init__(self, value, lineno = None):
        self.value = value
        self.lineno = lineno

class Continue(Node):
    def __init__(self, value, lineno = None):
        self.value = value
        self.lineno = lineno




class Error(Node):
    def __init__(self):
        pass



