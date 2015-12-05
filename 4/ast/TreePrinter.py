from AST import *


def addToClass(cls, *classes):
    def decorator(func):
        setattr(cls, func.__name__, func)
        for c in classes:
            setattr(c, func.__name__, func)
        return func

    return decorator


def convert(expression, identation):
    if expression.__class__.__name__ == "str":
        return branch_str(identation) + expression + "\n"
    else:
        return expression.printTree(identation)


def branch_str(level):
    return "| " * level


class TreePrinter:
    @addToClass(Program)
    def printTree(self, level):
        part_tree = ""
        for p in self.part:
            part_tree += p.printTree(1)
        return "PROGRAM\n" + part_tree

    @addToClass(Node)
    def printTree(self, level):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(Const)
    def printTree(self, level):
        return convert(str(self.value), level)

    @addToClass(Variable)
    def printTree(self, level):
        decl_str = convert("DECL", level)
        vars_str = "".join(map(lambda i: i.printTree(level + 1), self.variables))
        return decl_str + vars_str

    @addToClass(BinExpr, RelExpr, Declaration, Assignment)
    def printTree(self, level):
        operator_string = convert(self.op, level)
        left_expr = convert(self.left, level + 1)
        right_expr = convert(self.right, level + 1)
        return operator_string + left_expr + right_expr

    @addToClass(ChoiceInstruction)
    def printTree(self, level):
        if_statement_str = convert('IF', level)
        condition_str = convert(self.cond, level + 1)
        then_instr_str = convert(self.instr, level + 1)

        return if_statement_str + condition_str + then_instr_str

    @addToClass(ChoiceInstructionWithElse)
    def printTree(self, level):
        if_statement_str = convert('IF', level)
        condition_str = convert(self.cond, level + 1)
        then_instr_str = convert(self.instr, level + 1)

        if_then_str = if_statement_str + condition_str + then_instr_str
        else_statement_str = convert('ELSE', level)
        else_instr_str = convert(self.elinstr, level + 1)
        return if_then_str + else_statement_str + else_instr_str

    @addToClass(WhileLoop)
    def printTree(self, level):
        while_statement_str = convert('WHILE', level)
        condition_str = convert(self.cond, level + 1)
        do_instr_str = convert(self.instr, level + 1)

        return while_statement_str + condition_str + do_instr_str

    @addToClass(RepeatUntilLoop)
    def printTree(self, level):
        repeat_statement_str = convert('REPEAT', level)
        repeat_instr_str = "".join(map(lambda i: i.printTree(level + 1), self.instr))
        condition_str = convert(self.cond, level + 1)

        return repeat_statement_str + repeat_instr_str + condition_str

    @addToClass(Return)
    def printTree(self, level):
        return_str = convert('RETURN', level)
        value_str = convert(self.value, level + 1)

        return return_str + value_str

    @addToClass(Break)
    def printTree(self, level):
        return convert('BREAK', level)

    @addToClass(Continue)
    def printTree(self, level):
        return convert('CONTINUE', level)

    @addToClass(Print)
    def printTree(self, level):
        print_str = convert('PRINT', level)
        value_str = convert(self.expr, level + 1)
        return print_str + value_str

    @addToClass(FunctionDefinition)
    def printTree(self, level):
        fundef_str = convert('FUNDEF', level)
        name_str = convert(self.ident, level + 1)
        ret_str = convert('RET ' + self.typ, level + 1)
        args_str = "".join(map(lambda i: convert(i, level + 1), self.args))
        body_str = convert(self.instr, level + 1)

        return fundef_str + name_str + ret_str + args_str + body_str

    @addToClass(FunctionCall)
    def printTree(self, level):
        funcall_str = convert('FUNCALL', level)
        name_str = convert(self.ident, level + 1)
        args_str = "".join(map(lambda i: convert(i, level + 1), self.args))
        return funcall_str + name_str + args_str

    @addToClass(Argument)
    def printTree(self, level):
        return convert('ARG ' + self.ident, level)

    @addToClass(CompoundInstruction)
    def printTree(self, level):
        decl_str = "".join(map(lambda i: convert(i, level), self.decl))
        instr_str = "".join(map(lambda i: convert(i, level), self.instr))
        return decl_str + instr_str

    @addToClass(Label)
    def printTree(self, level):
        return convert(self.ident, level)
