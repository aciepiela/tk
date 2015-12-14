from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_branch(level):
    print("|" * level, end='')


class TreePrinter:
    def print_tree(self, node):
        node.printTree()

    @addToClass(AST.Node)
    def printTree(self, level):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, level=0):
        self.parts.printTree(level)

    @addToClass(AST.Parts)
    def printTree(self, level):
        if len(self.parts) > 0:
            for part in self.parts:
                print_branch(level)
                part.printTree(level + 1)

    @addToClass(AST.Declarations)
    def printTree(self, level):
        if len(self.declarations) > 0:
            print_branch(level)
            # print("DECL")
            for declaration in self.declarations:
                declaration.printTree(level + 1)

    @addToClass(AST.Declaration)
    def printTree(self, level):
        print("DECL")
        self.inits.printTree(level)

    @addToClass(AST.Inits)
    def printTree(self, level):
        for init in self.inits:
            init.printTree(level)

    @addToClass(AST.Init)
    def printTree(self, level):
        print_branch(level)
        print('=')
        print_branch(level + 1)
        print(self.id)
        self.expression.printTree(level + 1)

    @addToClass(AST.Instructions)
    def printTree(self, level):
        for instruction in self.instructions:
            instruction.printTree(level)

    @addToClass(AST.PrintInstruction)
    def printTree(self, level):
        print_branch(level)
        print('PRINT')
        self.expression.printTree(level + 1)

    @addToClass(AST.AssignementInstr)
    def printTree(self, level):
        print_branch(level)
        print('=')
        print_branch(level + 1)
        print(self.id)
        self.expression.printTree(level + 1)

    @addToClass(AST.IfInstruction)
    def printTree(self, level):
        print_branch(level)
        print('IF')
        self.condition.printTree(level + 1)
        self.instruction.printTree(level + 1)

    @addToClass(AST.IfElseInstruction)
    def printTree(self, level):
        print_branch(level)
        print('IF')
        self.condition.printTree(level + 1)
        self.instruction.printTree(level + 1)
        print_branch(level)
        print('ELSE')
        self.else_instruction.printTree(level + 1)

    @addToClass(AST.WhileInstruction)
    def printTree(self, level):
        print_branch(level)
        print("WHILE")
        self.condition.printTree(level + 1)
        self.instruction.printTree(level + 1)

    @addToClass(AST.RepeatInstr)
    def printTree(self, level):
        print_branch(level)
        print("REPEAT")
        self.instruction.printTree(level + 1)
        self.condition.printTree(level + 1)

    @addToClass(AST.ReturnInstr)
    def printTree(self, level):
        pass

    @addToClass(AST.ContinueInstr)
    def printTree(self, level):
        pass

    @addToClass(AST.BreakInstr)
    def printTree(self, level):
        pass

    @addToClass(AST.CompoundInstr)
    def printTree(self, level):
        self.declarations.printTree(level)
        self.instructions.printTree(level)

    @addToClass(AST.Condition)
    def printTree(self, level):
        self.expression.printTree(level)

    @addToClass(AST.IdExpression)
    def printTree(self, level):
        print_branch(level)
        print(self.id)

    @addToClass(AST.ConstExpression)
    def printTree(self, level):
        self.const.printTree(level)

    @addToClass(AST.BinaryOperatorExpression)
    def printTree(self, level):
        print_branch(level)
        print(self.symbol)
        self.left_expr.printTree(level + 1)
        self.right_expr.printTree(level + 1)

    @addToClass(AST.BracketExpression)
    def printTree(self, level):
        self.expression.printTree(level)

    @addToClass(AST.FuncallExpression)
    def printTree(self, level):
        print_branch(level)
        print('FUNCALL')
        print_branch(level + 1)
        print(self.id)
        self.expr_list_or_empty.printTree(level + 1)

    @addToClass(AST.ExpressionListOrEmpty)
    def printTree(self, level):
        if self.expression_list:
            self.expression_list.printTree(level)

    @addToClass(AST.ExpressionList)
    def printTree(self, level):
        for expression in self.expressions:
            expression.printTree(level)

    @addToClass(AST.FunDef)
    def printTree(self, level):
        print("FUNDEF")
        print_branch(level)
        print(self.id)
        print_branch(level)
        print("RET", self.type)
        self.arg_list_or_empty.printTree(level)
        self.compound_instr.printTree(level)

    @addToClass(AST.ArgListOrEmpty)
    def printTree(self, level):
        if self.arg_list:
            self.arg_list.printTree(level)

    @addToClass(AST.ArgList)
    def printTree(self, level):
        for arg in self.args:
            arg.printTree(level)

    @addToClass(AST.Argument)
    def printTree(self, level):
        print_branch(level)
        print('ARG', self.id)

    @addToClass(AST.Const)
    def printTree(self, level):
        print_branch(level)
        print(self.value)

    @addToClass(AST.InstructionsOpt)
    def printTree(self, level):
        self.instructions.printTree(level)
