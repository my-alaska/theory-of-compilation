from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)




    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        self.instr.printTree(indent)
        if self.next_instr:
            self.next_instr.printTree(indent)




    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))




    @addToClass(AST.Identifier)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)




    # @addToClass(AST.Function)
    # def printTree(self, indent=0):
    #     print("| " * indent + self.name)
    #     self.args.printTree(indent + 1)
    #
    # @addToClass(AST.FunctionArgs)
    # def printTree(self, indent=0):
    #     self.args.printTree(indent)
    #     if self.lastarg:
    #         self.lastarg.printTree(indent)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print("| " * indent + self.name)
        self.arg.printTree(indent + 1)




    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        self.print_body.printTree(indent + 1)


    @addToClass(AST.PrintBody)
    def printTree(self, indent=0):
        self.args.printTree(indent)
        if self.lastarg:
            self.lastarg.printTree(indent)




    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        print("| " * (indent + 1) + self.id)
        print("| " * (indent + 1) + "RANGE")
        self.expr1.printTree(indent + 2)
        self.expr2.printTree(indent + 2)
        self.instr.printTree(indent + 1)
        # fill in the body

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.expr.printTree(indent + 1)
        self.instr.printTree(indent + 1)
        # fill in the body

    @addToClass(AST.IfOrElse)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr1.printTree(indent + 1)
        if self.instr2:
            print("| " * indent + "ELSE")
            self.instr2.printTree(indent + 1)




    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print("| " * indent + self.assignment)
        self.left.printTree(indent + 1)
        self.val.printTree(indent + 1)




    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print("| " * indent + "MATRIX")
        if self.body:
            self.body.printTree(indent + 1)

    @addToClass(AST.MatrixBody)
    def printTree(self, indent=0):
        if self.lastvec:
            self.vecs.printTree(indent)
            print("| " * indent + "VECTOR")
            self.lastvec.printTree(indent+1)
        else:
            print("| " * indent + "VECTOR")
            self.vecs.printTree(indent+1)

    # @addToClass(AST.Vector)
    # def printTree(self, indent=0):
    #     print("| " * indent + "VECTOR")
    #     if self.body:
    #         self.body.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        self.items.printTree(indent)
        if self.next_item:
            self.next_item.printTree(indent)

    @addToClass(AST.MatrixAccess)
    def printTree(self, indent=0):
        print("| " * indent + "REF")
        self.name.printTree(indent + 1)
        self.arg1.printTree(indent + 1)
        self.arg2.printTree(indent + 1)





    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print("| " * indent + 'TRANSPOSE')
        self.arg.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print("| " * indent + '-')
        self.arg.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("| " * indent + "RETURN")
        if self.instr:
            self.instr.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("| " * indent + self.value)




    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
