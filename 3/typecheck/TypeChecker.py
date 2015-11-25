# -*- coding: utf-8 -*-

from ast.AST import *
from typecheck.SymbolTable import *
from typecheck.OperationsTable import OperationsTable as OT


class TypeChecker:
    def __init__(self):
        self.symbolTable = None
        self.operationsTable = OT()
        self.errors = 0

    def raiseError(self, body):
        self.errors += 1
        print body

    @staticmethod
    def typesAreCoherent(should, beType):
        return beType == should or (beType == 'float' and should == 'int')

    def acceptOrVar(self, node):
        if node.__class__.__name__ == 'str':
            variable = self.symbolTable.get(node)
            return None if variable is None else variable.type
        else:
            return node.accept(self)

    def analyzeParts(self, parts):
        for p in parts:
            if isinstance(p, Declaration) or isinstance(p, Variable):
                self.analyzeDeclarations([p])
            elif isinstance(p, FunctionDefinition):
                self.analyzeFunctionDeclarations([p])
            elif isinstance(p, CompoundInstruction):
                self.analyzeInstructionBlock([p])
            else:
                p.accept(self)

    def analyzeDeclarations(self, declarationsList):
        for varList in declarationsList:
            if varList.accept(self):
                Type = varList.typ
                for var in varList.variables:
                    try:
                        self.symbolTable.put(var.left, VariableSymbol(var.left, Type, var))
                    except Exception:
                        self.raiseError("Error: Variable '" + var.left + "' already declared: line " + str(var.lineno))

    def analyzeFunctionDeclarations(self, declarationsList):
        for funDef in declarationsList:
            try:
                self.symbolTable.put(funDef.ident, FunctionSymbol(funDef.ident, funDef.typ, funDef.args, funDef))
            except Exception:
                self.raiseError("Error: Redefinition of function '" + funDef.ident + "': line " + str(funDef.lineno))
            if funDef.accept(self) is None:
                self.raiseError("(linia " + str(funDef.lineno) + "): Bledna definicja funkcji " + funDef.ident + ".")

    def analyzeInstructionBlock(self, block):
        if isinstance(block, CompoundInstruction):
            return self.visit_CompoundInstruction(block)
        elif isinstance(block, list):
            return self.analyzeInstructions(block)
        elif isinstance(block, Node):
            return block.accept(self)
        else:
            raise Exception("co jeszcze?")

    def analyzeInstructions(self, instructionsList):
        for instr in instructionsList:
            instr.accept(self)

    def analyzeCondExpr(self, expr):
        condType = expr.accept(self)
        if condType != 'int':
            self.raiseError("(linia " + str(expr.lineno) + "): Nieprawidlowe wyrazenie warunkowe.")

    def visit_BinExpr(self, node):
        leftType = self.acceptOrVar(node.left)
        rightType = self.acceptOrVar(node.right)
        op = node.op
        if leftType is None:
            self.raiseError("(linia " + str(node.lineno) + "): Nie obslugiwany typ lewej strony.")
        if rightType is None:
            self.raiseError("(linia " + str(node.lineno) + "): Nie obslugiwany typ prawej strony.")
        if rightType is not None and leftType is not None:
            Type = self.operationsTable.getOperationType(op, leftType, rightType)
            if Type is None:
                self.raiseError(
                    "Error: Illegal operation, " + leftType + " " + op + " " + rightType + ": line " + str(node.lineno))
            return Type

    def visit_Assignment(self, assInstr):
        if assInstr.left.__class__.__name__ != 'str':
            self.raiseError("(linia " + str(assInstr.lineno) + "): Lewa strona przypisania musi byc identyfikatorem.")
        leftType = self.acceptOrVar(assInstr.left)
        rightType = self.acceptOrVar(assInstr.right)
        if leftType is None:
            self.raiseError(
                "Error: Variable '" + assInstr.left + "' undefined in current scope: line " + str(assInstr.lineno))
        if rightType is None:
            self.raiseError("(linia " + str(assInstr.lineno) + "): Nie obslugiwany typ wartosci przypisywanej.")
        if rightType is not None and leftType is not None:
            if (leftType == 'int' and rightType == 'float'):
                print("Ostrzezenie (linia " + str(
                    assInstr.lineno) + ") Przypisanie float do int, mozliwa utrata dokladnosci")
            elif not TypeChecker.typesAreCoherent(should=rightType, beType=leftType):
                self.raiseError("(linia " + str(
                    assInstr.lineno) + "): Zly typ wartości przypisywanej, wymagany " + leftType + ", znaleziony " + rightType + ".")

    def visit_CompoundInstruction(self, compInstr):
        prevTable = self.symbolTable
        self.symbolTable = SymbolTable(prevTable, "compInstr(" + str(compInstr.lineno) + ") scope")
        self.analyzeDeclarations(compInstr.decl)
        self.analyzeInstructionBlock(compInstr.instr)
        symbolTable = self.symbolTable
        self.symbolTable = prevTable
        return symbolTable

    def visit_WhileLoop(self, whLoop):
        self.analyzeCondExpr(whLoop.cond)
        whLoop.instr.accept(self)

    def visit_RepeatUntilLoop(self, repeatLoop):
        self.analyzeInstructionBlock(repeatLoop.instr)
        self.analyzeCondExpr(repeatLoop.cond)

    def visit_RelExpr(self, node):
        type1 = self.acceptOrVar(node.left)
        type2 = self.acceptOrVar(node.right)
        op = node.op
        if type1 is None:
            self.raiseError("(linia " + str(node.lineno) + "): Nie obslugiwany typ wyrazenia po lewej.")
        if type2 is None:
            self.raiseError("(linia " + str(node.lineno) + "):  Nie obslugiwany typ wyrazenia po prawej.")
        return self.operationsTable.getOperationType(op, type1, type2)

    def visit_Program(self, program):
        self.symbolTable = SymbolTable(None, "program scope")
        self.analyzeParts(program.part)
        return self.errors is 0

    def visit_Variable(self, variable):
        Type = variable.typ
        result = True
        for var in variable.variables:
            valueType = var.right.accept(self)
            if (Type == 'int' and valueType == 'float'):
                print("Ostrzezenie (linia " + str(
                    var.lineno) + ") Przypisanie float do int, mozliwa utrata dokladnosci")
            elif not TypeChecker.typesAreCoherent(should=valueType, beType=Type):
                self.raiseError("Error: Assigment of " + valueType + " to " + Type + ": line " + str(var.lineno))
                result = False
        return result

    def visit_Float(self, var):
        return 'float'

    def visit_Integer(self, var):
        return 'int'

    def visit_String(self, var):
        return 'string'

    def visit_Print(self, instr):
        Type = self.acceptOrVar(instr.expr)
        if Type is None:
            self.raiseError("Error: Usage of undeclared variable '" + instr.expr + "': line " + str(instr.lineno))

    def visit_Argument(self, arg):
        return arg.typ

    def visit_FunctionCall(self, funCall):
        funDef = self.symbolTable.get(funCall.ident)
        if funDef is None:
            self.raiseError("Error: Call of undefined fun: '" + funCall.ident + "': line " + str(funCall.lineno))
            return None
        if len(funDef.args) != len(funCall.args):
            self.raiseError("Error: Improper number of args in " + funCall.ident + ": line " + str(funCall.lineno))
            return funDef.type
        for left, right in zip(funDef.args, funCall.args):
            defType = left.accept(self)
            callType = self.acceptOrVar(right)
            if not TypeChecker.typesAreCoherent(should=callType, beType=defType):
                self.raiseError("Error: Improper type of args in " + funCall.ident + ": line " + str(funCall.lineno))
        return funDef.type

    def visit_ChoiceInstruction(self, instr):
        self.analyzeCondExpr(instr.cond)
        self.analyzeInstructionBlock(instr.instr)

    def visit_ChoiceInstructionWithElse(self, instr):
        self.visit_ChoiceInstruction(instr)
        self.analyzeInstructionBlock(instr.elinstr)

    def visit_FunctionDefinition(self, funDef):
        prevTable = self.symbolTable
        self.symbolTable = SymbolTable(prevTable, "fundef(" + funDef.ident + ") scope")

        for arg in funDef.args:
            self.symbolTable.put(arg.ident, VariableSymbol(arg.ident, arg.typ, arg))

        functionsBodySymbolTable = self.analyzeInstructionBlock(funDef.instr)

        self.symbolTable = functionsBodySymbolTable

        instrs = filter(lambda x: x.__class__.__name__ == 'Return', funDef.instr.instr)
        if len(instrs) == 0:
            self.raiseError("Error: Missing return statement in function '" + funDef.ident + "' returning " + funDef.typ
                            + ": line " + str(funDef.lineno))  # TODO
        else:
            for retInstr in instrs:
                valueType = retInstr.accept(self)
                if valueType is None:
                    a = 5
                # self.raiseError("Error: Incorrect return type, used undeclared function: '" + retInstr.ident + "': line " + str(
                #     retInstr.lineno))
                # print "(linia " + str(
                #     retInstr.lineno) + "): Zly zwracany typ, uzyto niezadeklarowanej zmiennej", retInstr.value
                elif valueType != funDef.typ:
                    print "(linia " + str(
                        retInstr.lineno) + "): Zly zwracany typ, wymagany", funDef.typ + ", znaleziony", valueType

        self.symbolTable = prevTable

        return funDef.typ

    def visit_Return(self, ret):
        return self.acceptOrVar(ret.value)
