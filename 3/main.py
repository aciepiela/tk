# -*- coding: utf-8 -*-

import sys

import ply.yacc as yacc

from ast.Cparser import Cparser
from typecheck.TypeChecker import TypeChecker
import ast.TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "tests/vars_undef.in"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()

    ast = parser.parse(text, lexer=Cparser.scanner)
    # print(ast)

    checker = TypeChecker()
    ast.accept(checker)

# Nie dziala control_transfer, funs3,funs6
