class Node(object):
    def __init__(self, type, lineno):
        self.type = type
        self.lineno = lineno

    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__
        method = getattr(visitor, method_name, None)
        if method is not None:
            return method(self)
        else:
            return None

    def __str__(self):
        return self.printTree(0)

    def accept_interpreter(self, visitor):
        return visitor.visit(self)

class Const(Node):
    def __init__(self, value, typ, lineno):
        Node.__init__(self, "const", lineno)
        self.value = value
        self.type = typ


class Integer(Const):
    def __init__(self, value, lineno):
        Const.__init__(self, int(value), "INTEGER", lineno)


class Float(Const):
    def __init__(self, value, lineno):
        Const.__init__(self, float(value), "FLOAT", lineno)


class String(Const):
    def __init__(self, value, lineno):
        Const.__init__(self, value, "STRING", lineno)


class Variable(Node):
    def __init__(self, typ, variables, lineno):
        Node.__init__(self, "var", lineno)
        self.typ = typ
        self.variables = variables


class BinExpr(Node):
    def __init__(self, left, op, right, lineno):
        Node.__init__(self, "binexpr", lineno)
        self.left = left
        self.right = right
        self.op = op


class RelExpr(Node):
    def __init__(self, left, op, right, lineno):
        Node.__init__(self, "relexpr", lineno)
        self.left = left
        self.right = right
        self.op = op


class Declaration(Node):
    def __init__(self, left, op, right, lineno):
        Node.__init__(self, "decl", lineno)
        self.left = left
        self.right = right
        self.op = op


class Assignment(Node):
    def __init__(self, left, op, right, lineno):
        Node.__init__(self, "=", lineno)
        self.left = left
        self.right = right
        self.op = op


class ChoiceInstruction(Node):
    def __init__(self, cond, instr, lineno):
        Node.__init__(self, "if", lineno)
        self.cond = cond
        self.instr = instr


class ChoiceInstructionWithElse(Node):
    def __init__(self, cond, instr, elinstr, lineno):
        Node.__init__(self, "ifelse", lineno)
        self.cond = cond
        self.instr = instr
        self.elinstr = elinstr


class WhileLoop(Node):
    def __init__(self, cond, instr, lineno):
        Node.__init__(self, "while", lineno)
        self.cond = cond
        self.instr = instr


class RepeatUntilLoop(Node):
    def __init__(self, instr, cond, lineno):
        Node.__init__(self, "repeat", lineno)
        self.cond = cond
        self.instr = instr


class Return(Node):
    def __init__(self, value, lineno):
        Node.__init__(self, "return", lineno)
        self.value = value


class Break(Node):
    def __init__(self, lineno):
        Node.__init__(self, "break", lineno)


class Continue(Node):
    def __init__(self, lineno):
        Node.__init__(self, "continue", lineno)


class Print(Node):
    def __init__(self, expr, lineno):
        Node.__init__(self, "print", lineno)
        self.expr = expr


class FunctionDefinition(Node):
    def __init__(self, typ, ident, args, instr, lineno):
        Node.__init__(self, "fundef", lineno)
        self.typ = typ
        self.ident = ident
        self.args = args
        self.instr = instr


class FunctionCall(Node):
    def __init__(self, ident, args, lineno):
        Node.__init__(self, "funcall", lineno)
        self.ident = ident
        self.args = args


class Argument(Node):
    def __init__(self, typ, ident, lineno):
        Node.__init__(self, "arg", lineno)
        self.typ = typ
        self.ident = ident


class CompoundInstruction(Node):
    def __init__(self, decl, instr, lineno):
        Node.__init__(self, "comp", lineno)
        self.decl = decl
        self.instr = instr


class Label(Node):
    def __init__(self, ident, instr, lineno):
        Node.__init__(self, "label", lineno)
        self.ident = ident
        self.instr = instr


class Program(Node):
    def __init__(self, part, lineno):
        Node.__init__(self, "program", lineno)
        self.part = part


class Part(Node):
    def __init__(self, lineno):
        Node.__init__(self, "part", lineno)
        self.lineno = lineno
