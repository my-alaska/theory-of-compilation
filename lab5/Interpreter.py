import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


def basicbin(f,left,right):
    if not isinstance(left,list): return f(left,right)
    if len(left) == 0: return []
    if not isinstance(left[0],list): return [f(left[i],right[i]) for i in range(len(left))]
    return [[f(left[i][j],right[i][j]) for j in range(len(left[0]))] for i in range(len(left))]


def mul(left, right):
    if not isinstance(left, list):
        return left*right
    res = [[0 for _ in range(len(left))] for _ in range(len(right[0]))]
    for i in range(len(left)):
        for j in range(len(right[0])):
            for k in range(len(right)):
                res[i][j] += left[i][k] * right[k][j]
    return res


def dot(f, left, right):
    if isinstance(right, list) and isinstance(left,list):
        if len(left) == 0: return [[]]
        if not isinstance(left[0],list): return [f(left[i],right[i]) for i in range(len(left))]
        return [[f(left[i][j],right[i][j]) for j in range(len(left[0]))] for i in range(len(left))]
    if isinstance(right,list):
        right,left = left,right
    if len(left) == 0: return []
    if not isinstance(left[0],list): return [f(left[i], right) for i in range(len(left))]
    return [[f(left[i][j], right) for j in range(len(left[0]))] for i in range(len(left))]


def atomadd(a,b): return a+b
def atomsub(a,b): return a-b
def atommul(a,b): return a*b
def atomdiv(a,b): return a/b

def add(a,b): return basicbin(atomadd,a,b)
def sub(a,b): return basicbin(atomsub,a,b)
def div(a,b): return basicbin(atomdiv,a,b)

def dotadd(a,b): return dot(atomadd,a,b)
def dotsub(a,b): return dot(atomsub,a,b)
def dotmul(a,b): return dot(atommul,a,b)
def dotdiv(a,b): return dot(atomdiv,a,b)

def eq(a, b): return a.__str__() == b.__str__()
def noteq(a, b): return a.__str__() != b.__str__()
def greater(a, b): return a > b
def less(a, b): return a < b
def greatereq(a, b): return a >= b
def lesseq(a, b): return a <= b

opdict = {  '+': add,
            '-': sub,
            '*': mul,
            '/': div,
            '.+': dotadd,
            '.-': dotsub,
            '.*': dotmul,
            './': dotdiv,
            '==': eq,
            '!=': noteq,
            '>': greater,
            '<': less,
            '>=': greatereq,
            '<=': lesseq}

class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self,node):
        node.instr.accept(self)
        if node.next_instr:
            node.next_instr.accept(self)




    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value




    @when(AST.Identifier)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return opdict[node.op](left, right)




    @when(AST.Function)
    def visit(self, node):
        size = node.arg.accept(self)
        if node.name == 'eye': return [[1 if i == j else 0 for i in range(size)] for j in range(size)]
        elif node.name == 'zeros': return [[ 0 for _ in range(size)] for _ in range(size)]
        elif node.name == 'ones': return [[ 1 for _ in range(size)] for _ in range(size)]




    @when(AST.Print)
    def visit(self, node):
        node.print_body.accept(self)

    @when(AST.PrintBody)
    def visit(self,node):
        to_print = []
        body = node
        while isinstance(body,AST.PrintBody):
            if body.lastarg is None: break
            to_print.append(body.lastarg.accept(self))
            body = body.args
        to_print.append(body.args.accept(self))
        to_print.reverse()
        print(*to_print, sep=', ')




    # TODO check for errors
    @when(AST.For)
    def visit(self, node):
        identifier = node.id
        expr1 = node.expr1.accept(self)
        expr2 = node.expr2.accept(self)
        self.memory.push("for")
        self.memory.insert(identifier, expr1)
        while self.memory.get(identifier) < expr2:
            try:
                self.memory.push(None)
                node.instr.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            finally:
                self.memory.set(identifier, self.memory.get(identifier) + 1)
                self.memory.pop()
        self.memory.pop()

    @when(AST.While)
    def visit(self, node):
        while node.expr.accept(self):
            try:
                self.memory.push(None)
                node.instr.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            finally:
                self.memory.pop()

    @when(AST.IfOrElse)
    def visit(self, node):
        expr = node.expr.accept(self)
        if expr:
            self.memory.push(None)
            node.instr1.accept(self)
            self.memory.pop()
        elif node.instr2 is not None:
            self.memory.push(None)
            node.instr2.accept(self)
            self.memory.pop()




    @when(AST.Assign)
    def visit(self, node):
        if isinstance(node.left, AST.MatrixAccess):
            matrix = self.memory.get(node.left.name.name)
            x = node.left.arg1.accept(self)
            y = node.left.arg2.accept(self)
            if node.assignment == '=':
                matrix[x][y] = node.val.accept(self)
            else:
                matrix[x][y] = opdict[node.assign[0]](matrix[x][y],node.val.accept(self))
            self.memory.set(node.left.name.name, matrix)
        else:
            if node.assignment == '=':
                self.memory.set(node.left.name, node.val.accept(self))
            else:
                var = self.memory.get(node.left.name)
                self.memory.set(node.left.name, opdict[node.assignment[0]](var, node.val.accept(self)))




    @when(AST.Matrix)
    def visit(self, node):
        body = node.body
        result = []
        while isinstance(body,AST.MatrixBody):
            if body.lastvec is None: break
            result.append(body.lastvec.accept(self))
            body = body.vecs
        result.append(body.vecs.accept(self))
        result.reverse()
        return result

    @when(AST.Vector)
    def visit(self, node):
        items = node.items
        result = []
        while isinstance(items, AST.Vector):
            if items.next_item is None: break
            result.append(items.next_item.accept(self))
            items = items.items
        result.append(items.items.accept(self))
        result.reverse()
        return result

    @when(AST.MatrixAccess)
    def visit(self, node):
        var = self.memory.get(node.name.name)
        x = node.arg1.accept(self)
        y = node.arg2.accept(self)
        return var[x][y]





    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()


