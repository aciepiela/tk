class Node(object):
    pass


class Program(Node):
    def __init__(self, parts):
        self.parts = parts


class Parts(Node):
    def __init__(self, parts):
        self.parts = parts  # list of parts


class Part(Node):
    pass


class Declarations(Node):
    def __init__(self, declarations):
        self.declarations = declarations  # list of Declaration


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type  # Type class
        self.inits = inits  # Inits class


class Inits(Node):
    def __init__(self, inits):
        self.inits = inits  # list of Init


class Init(Node):
    def __init__(self, id, expression):
        self.id = id  # Type class
        self.expression = expression  # Expression class


class InstructionsOpt(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions  # list of Instruction


class Instruction(Node):
    pass


class PrintInstruction(Instruction):
    def __init__(self, expression):
        self.expression = expression  # Expression class


class LabeledInstruction(Instruction):
    def __init__(self, id, instruction):
        self.id = id  # Id class
        self.instruction = instruction  # Instruction class


class AssignementInstr(Instruction):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class IfInstruction(Instruction):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class IfElseInstruction(IfInstruction):
    def __init__(self, condition, instruction, else_instruction):
        super(IfElseInstruction, self).__init__(condition, instruction)
        self.else_instruction = else_instruction


class WhileInstruction(Instruction):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstr(Instruction):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition


class ReturnInstr(Instruction):
    def __init__(self, expression):
        self.expression = expression


class ContinueInstr(Instruction):
    pass


class BreakInstr(Instruction):
    pass


class CompoundInstr(Instruction):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


class Condition(Node):
    def __init__(self, expression):
        self.expression = expression


class Expression(Node):
    pass


class IdExpression(Expression):
    def __init__(self, id):
        self.id = id


class ConstExpression(Expression):
    def __init__(self, const):
        self.const = const


class BinaryOperatorExpression(Expression):
    def __init__(self, symbol, left_expr, right_expr):
        self.symbol = symbol
        self.left_expr = left_expr
        self.right_expr = right_expr


class AddExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(AddExpression, self).__init__('+', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class SubtractExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(SubtractExpression, self).__init__('-', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class MultiplyExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(MultiplyExpression, self).__init__('*', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class DivideExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(DivideExpression, self).__init__('/', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class ModuloExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(ModuloExpression, self).__init__('%', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class BinOrExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(BinOrExpression, self).__init__('|', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class BinAndExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(BinAndExpression, self).__init__('&', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class BinXorExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(BinXorExpression, self).__init__('^', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class AndExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(AndExpression, self).__init__('&&', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class OrExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(OrExpression, self).__init__('||', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class EqualExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(EqualExpression, self).__init__('==', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class NotEqualExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(NotEqualExpression, self).__init__('!=', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class LowerExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(LowerExpression, self).__init__('<', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class GreaterExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(GreaterExpression, self).__init__('>', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class LowerEqualExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(LowerEqualExpression, self).__init__('<=', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class GreaterEqualExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(GreaterEqualExpression, self).__init__('>=', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class SHRExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(SHRExpression, self).__init__('>>', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class SHLExpression(BinaryOperatorExpression):
    def __init__(self, left_expr, right_expr):
        super(SHLExpression, self).__init__('<<', left_expr, right_expr)
        self.left_expr = left_expr
        self.right_expr = right_expr


class BracketExpression(Expression):
    def __init__(self, expression):
        self.expression = expression


class FuncallExpression(Expression):
    def __init__(self, id, expr_list_or_empty):
        self.id = id
        self.expr_list_or_empty = expr_list_or_empty


class ExpressionListOrEmpty(Node):
    def __init__(self, expression_list):
        self.expression_list = expression_list


class ExpressionList(Node):
    def __init__(self, expressions):
        self.expressions = expressions


class FunDef(Node):
    def __init__(self, type, id, arg_list_or_empty, compound_instr):
        self.type = type
        self.id = id
        self.arg_list_or_empty = arg_list_or_empty
        self.compound_instr = compound_instr


class ArgListOrEmpty(Node):
    def __init__(self, arg_list):
        self.arg_list = arg_list


class ArgList(Node):
    def __init__(self, args):
        self.args = args


class Argument(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    def __init__(self, value):
        super(Integer, self).__init__(value)


class Float(Const):
    def __init__(self, value):
        super(Float, self).__init__(value)


class String(Const):
    def __init__(self, value):
        super(String, self).__init__(value)


class Error(Node):
    def __init__(self, error):
        self.error = error
