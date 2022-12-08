#!/usr/bin/python


import AST
from SymbolTable import *

from collections import defaultdict
from functools import reduce

type_dict = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: None
        )
    )
)

type_dict["+"]["int"]["int"] = "int"
type_dict["-"]["int"]["int"] = "int"
type_dict["*"]["int"]["int"] = "int"
type_dict["/"]["int"]["int"] = "int"

type_dict['<']["int"]["int"] = "bool"
type_dict['>']["int"]["int"] = "bool"
type_dict["<="]["int"]["int"] = "bool"
type_dict[">="]["int"]["int"] = "bool"
type_dict["=="]["int"]["int"] = "bool"
type_dict["!="]["int"]["int"] = "bool"

type_dict["+"]["int"]["float"] = "float"
type_dict["-"]["int"]["float"] = "float"
type_dict["*"]["int"]["float"] = "float"
type_dict["/"]["int"]["float"] = "float"

type_dict["<"]["int"]["float"] = "bool"
type_dict[">"]["int"]["float"] = "bool"
type_dict["<="]["int"]["float"] = "bool"
type_dict[">="]["int"]["float"] = "bool"
type_dict["=="]["int"]["float"] = "bool"
type_dict["!="]["int"]["float"] = "bool"

type_dict["+"]["float"]["int"] = "float"
type_dict["-"]["float"]["int"] = "float"
type_dict["*"]["float"]["int"] = "float"
type_dict["/"]["float"]["int"] = "float"

type_dict["<"]["float"]["int"] = "bool"
type_dict[">"]["float"]["int"] = "bool"
type_dict["<="]["float"]["int"] = "bool"
type_dict[">="]["float"]["int"] = "bool"
type_dict["=="]["float"]["int"] = "bool"
type_dict["!="]["float"]["int"] = "bool"

type_dict["+"]["float"]["float"] = "float"
type_dict["-"]["float"]["float"] = "float"
type_dict["*"]["float"]["float"] = "float"
type_dict["/"]["float"]["float"] = "float"

type_dict["<"]["float"]["float"] = "bool"
type_dict[">"]["float"]["float"] = "bool"
type_dict["<="]["float"]["float"] = "bool"
type_dict[">="]["float"]["float"] = "bool"
type_dict["=="]["float"]["float"] = "bool"
type_dict["!="]["float"]["float"] = "bool"

type_dict["+"]["vector"]["vector"] = "vector"
type_dict["-"]["vector"]["vector"] = "vector"
type_dict["*"]["vector"]["vector"] = "vector"
type_dict["/"]["vector"]["vector"] = "vector"

type_dict["+="]["vector"]["vector"] = "vector"
type_dict["-="]["vector"]["vector"] = "vector"
type_dict["*="]["vector"]["vector"] = "vector"
type_dict["/="]["vector"]["vector"] = "vector"

type_dict[".+"]["vector"]["vector"] = "vector"
type_dict[".+"]["vector"]["int"] = "vector"
type_dict[".+"]["vector"]["float"] = "vector"
type_dict[".+"]["int"]["vector"] = "vector"
type_dict[".+"]["float"]["vector"] = "vector"

type_dict[".-"]["vector"]["vector"] = "vector"
type_dict[".-"]["vector"]["int"] = "vector"
type_dict[".-"]["vector"]["float"] = "vector"
type_dict[".-"]["int"]["vector"] = "vector"
type_dict[".-"]["float"]["vector"] = "vector"

type_dict[".*"]["vector"]["vector"] = "vector"
type_dict[".*"]["vector"]["int"] = "vector"
type_dict[".*"]["vector"]["float"] = "vector"
type_dict[".*"]["int"]["vector"] = 'vector'
type_dict[".*"]["float"]["vector"] = 'vector'

type_dict["./"]["vector"]["vector"] = "vector"
type_dict["./"]["vector"]["int"] = "vector"
type_dict["./"]["vector"]["float"] = "vector"
type_dict["./"]["int"]["vector"] = "vector"
type_dict["./"]["float"]["vector"] = "vector"

type_dict["+"]["string"]["string"] = "string"

type_dict["\'"]["vector"][None] = "vector"
type_dict["-"]["vector"][None] = "vector"
type_dict["-"]["int"][None] = "int"
type_dict["-"]["float"][None] = "float"


class NodeVisitor(object):

    def __init__(self):
        self.symbol_table = SymbolTable(None, "table name")

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable(None, 'main')
        self.loopcount = 0




    def visit_Instructions(self, node):
        self.visit(node.instr)
        if node.next_instr:
            self.visit(node.next_instr)




    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return "string"




    def visit_Identifier(self, node):
        return self.symbol_table.get(node.name)
        # self.visit(node.name) # TODO u sure??

    # comparison is treated as BinExpr
    def visit_BinExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        type_ = type_dict[op][str(left)][str(right)]
        if type_ == "vector":
            if str(left) == 'vector' and str(right) == 'vector':
                if left.size != right.size:
                    print("vector size mismatch at bin expr  : ", node.lineno)
                elif left.type_ != right.type_:
                    print("vector type mismatch at bin expr  : ", node.lineno)
        elif type_ is None:
            print("binary expression error: ", node.lineno)
            return None
        else:
            return type_




    def visit_Function(self, node):
        if str(self.visit(node.arg)) == 'int':
            return VarSymbol(None, 'int', 2, size=(node.arg.value, node.arg.value))
        print("Invalid matrix function: ", node.lineno)
        return None




    def visit_Print(self, node):
        self.visit(node.print_body.args)


    def visit_PrintBody(self,node):
        self.visit(node.args)
        if node.lastarg:
            self.visit(node.lastarg)



    def visit_For(self, node):
        self.loopcount += 1
        self.symbol_table = self.symbol_table.pushScope("For")
        type1 = self.visit(node.expr1)
        type2 = self.visit(node.expr2)
        if type1 is None or type2 is None:
            print("invalid for loop range: ", node.lineno)

        if str(type1) != 'int' or str(type2) != 'int':
            print("invalid for loop access: ", node.lineno)
            t = None
        else:
            t = "int"
        self.symbol_table.put(node.id, VarSymbol(node.id, t))
        self.visit(node.instr)
        self.loopcount -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_While(self, node):
        self.loopcount += 1
        self.symbol_table = self.symbol_table.pushScope("While")
        self.visit(node.expr)
        self.visit(node.instr)
        self.loopcount -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_IfOrElse(self, node):
        self.visit(node.expr)
        self.symbol_table = self.symbol_table.pushScope("If")
        self.visit(node.instr1)
        self.symbol_table = self.symbol_table.popScope()
        if node.instr2:
            self.symbol_table.pushScope("else")
            self.visit(node.instr2)
            self.symbol_table.popScope()




    def visit_Assign(self, node):
        val = self.visit(node.val)  # TODO returns node or type?!?!

        if val is None:
            return None
        assignment = node.assignment
        if assignment == "=":
            self.symbol_table.put(node.left.name, val)
        else:
            left = self.visit(node.left)
            if left is None:
                print("invalid identifier when assigning: ", node.lineno)
                return None
            type_ = type_dict[assignment][str(left)][str(val)]
            if left.dim != 0 and val.dim != 0:
                if left.size != val.size:
                    print("vector size mismatch at assignment: ", node.lineno)
                    return None
            elif type_ is None:
                print("assignment error: ", node.lineno)
                return None
            else: return type_




    def visit_Matrix(self, node):
        body = node.body
        m_len = 0
        v_len = -1
        prev_type = None
        now_type = None

        def f(v):
            nonlocal m_len, prev_type, v_len

            vector = self.visit(v)
            m_len += 1
            if vector is None:
                print("illegal None vector: ", node.lineno)
                return None
            now_type = vector.type_
            if now_type != prev_type and prev_type is not None:
                print("Matrix type mismatch: ", v.lineno)
                return None
            prev_type = now_type
            if v_len == -1:
                v_len = vector.size
            elif v_len != vector.size:
                print("Matrix vector size mismatch: ", v.lineno)
                return None
            if vector.dim != 1:
                print("Wrong dimension: ", v.lineno)

        while isinstance(body,AST.MatrixBody):
            if body.lastvec is None: break
            f(body.lastvec)
            body = body.vecs
        f(body.vecs)


        return VarSymbol(None, now_type, 2, size=(m_len, v_len))

        # while body != None:
        #     vector = self.visit(body.lastvec)
        #     m_len += 1
        #     if vector is None:
        #         print("illegal None vector: ", node.lineno)
        #         return None
        #     now_type = vector.type_
        #     if now_type != prev_type and prev_type is not None:
        #         print("Matrix type mismatch: ", body.lastvec.lineno)
        #         return None
        #     prev_type = now_type
        #     if v_len == -1:
        #         v_len = vector.size
        #     elif v_len != vector.size:
        #         print("Matrix vector size mismatch: ", body.lastvec.lineno)
        #         return None
        #     if vector.dim != 1:
        #         print("Wrong dimension: ", body.lastvec.lineno)
        #     body = body.vecs
        # return VarSymbol(None, now_type, 2, size=(m_len, v_len))

    def visit_Vector(self, node):
        items = node.items
        prev_type = None
        now_type = None

        size = 0

        def f(i):
            nonlocal size,prev_type
            var = self.visit(i)
            now_type = str(var)
            size += 1
            if (now_type != 'int' and now_type != 'float') or (prev_type != None and now_type != prev_type):
                print("Vector type mismatch: ", i.lineno)
                return None
            prev_type = now_type

        while isinstance(items,AST.Vector):
            if items.next_item == None: break
            f(items.next_item)
            items = items.items
        f(items.items)

        return VarSymbol(None, now_type, 1, size=(size, 1))

    # def visit_VectorBody(self,node):


    def visit_MatrixAccess(self, node):
        if str(self.visit(node.arg1)) != 'int' or str(self.visit(node.arg1)) != 'int':
            print("Invalid matrix access: ", node.lineno)
            return None
        return self.visit(node.name)





    def visit_Transpose(self, node):
        vector = self.visit(node.arg)
        if str(vector) != 'vector':
            print("Invalid object transposition: ", node.lineno)
            return None
        if vector.dim == 1 or vector.dim == 2:
            return VarSymbol(None, vector.type_, vector.dim, size=(vector.size[1], vector.size[0]))
        else:
            print("invalid vector dimension: ", node.lineno)
            return None

    def visit_UnaryMinus(self, node):
        expr = self.visit(node.arg)
        expr_type = self.symbol_table['-'][expr][None]  # TODO maybe str() ???
        if expr_type is None:
            print("invalid type for uminus operation: ", node.lineno)

    def visit_Return(self, node):
        return self.visit(node.instr)

    def visit_BreakContinue(self, node):
        if self.loopcount == 0:
            print("Break/Continue outside of loop: ", node.lineno)
