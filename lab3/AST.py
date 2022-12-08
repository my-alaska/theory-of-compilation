class Node(object):
    pass




class Instructions(Node):
    def __init__(self, instr, next_instr=None):
        self.instr = instr
        self.next_instr = next_instr




class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):

    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value




class Identifier(Node):
    def __init__(self, id):
        self.id = id

class BinExpr(Node):
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right




class Function(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class FunctionArgs(Node):
    def __init__(self, args, lastarg=None):
        self.args = args
        self.lastarg = lastarg




class Print(Node):
    def __init__(self, print_body):
        self.print_body = print_body

class PrintBody(Node):
    def __init__(self, args, lastarg=None):
        self.args = args
        self.lastarg = lastarg




class For(Node):
    def __init__(self, id, expr1, expr2, instr):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2
        self.instr = instr

class While(Node):
    def __init__(self, expr, instr):
        self.expr = expr
        self.instr = instr

class IfOrElse(Node):
    def __init__(self, expr, instr1, instr2=None):
        self.expr = expr
        self.instr1 = instr1
        self.instr2 = instr2




class Assign(Node):
    def __init__(self, left, assignment, val):
        self.left = left
        self.assignment = assignment
        self.val = val




class Matrix(Node):
    def __init__(self, body=None):
        self.body = body

class Vector(Node):
    def __init__(self, vecs, lastvec=None):
        self.vecs = vecs
        self.lastvec = lastvec

# class Vector(Node):
#     def __init__(self, body=None):
#         self.body = body

class VectorBody(Node):
    def __init__(self, item, next_item=None):
        self.item = item
        self.next_item = next_item

class MatrixAccess(Node):
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args




class Transpose(Node):
    def __init__(self, arg):
        self.arg = arg

class UnaryMinus(Node):
    def __init__(self, arg):
        self.arg = arg

class Return(Node):
    def __init__(self, instr=None):
        self.instr = instr

class BreakContinue(Node):
    def __init__(self, value):
        self.value = value




class Error(Node):
    def __init__(self):
        pass



