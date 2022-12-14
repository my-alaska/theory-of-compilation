# import sys
# import ply.yacc as yacc
# # from Mparser import Mparser
# import Mparser
# from TreePrinter import TreePrinter
#
#
# if __name__ == '__main__':
#
#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example3.m"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)
#
#     # Mparser = Mparser()
#     parser = yacc.yacc(module=Mparser)
#     text = file.read()
#     ast = parser.parse(text, lexer=Mparser.scanner.lexer) # .scanner
#     ast.printTree()


import sys
import ply.yacc as yacc
# from Mparser import Mparser
import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "incorrect\\opers.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner.lexer)

    # Below code shows how to use visitor
    ast.printTree()

    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

