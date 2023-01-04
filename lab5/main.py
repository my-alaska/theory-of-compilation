import sys
import ply.yacc as yacc
import Mparser
from TreePrinter import TreePrinter
import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/fibonacci.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner.lexer)

    if not Mparser.ERRORS:
        # Below code shows how to use visitor
        typeChecker = TypeChecker.TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

        if not TypeChecker.ERRORS:
            ast.accept(Interpreter())
        else: print("Type checker errors !!!")
        # in future
        # ast.accept(OptimizationPass1())
        # ast.accept(OptimizationPass2())
        # ast.accept(CodeGenerator())
    else: print("Syntax errors")
