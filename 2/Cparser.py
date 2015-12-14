#!/usr/bin/python
from AST import *

from scanner import Scanner


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print('At end of input')

    def p_program(self, p):
        """program : parts """
        p[0] = Program(p[1])

    def p_parts(self, p):
        """parts : part parts
                 | part """
        if len(p) == 3:
            result = []
            result.append(p[1])
            result.extend(p[2].parts)
            p[0] = Parts(result)
        else:
            p[0] = Parts([p[1]])

    def p_part(self, p):
        """part : fundef
                | instruction
                | declaration """
        p[0] = p[1]

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) == 3:
            result = []
            result.extend(p[1].declarations)
            result.append(p[2])
            p[0] = Declarations(result)
        else:
            p[0] = Declarations([])

    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        if len(p) == 4:
            p[0] = Declaration(p[1], p[2])
        else:
            p[0] = Error(p[1])

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            result = []
            result.extend(p[1].inits)
            result.append(p[3])
            p[0] = Inits(result)
        else:
            p[0] = Inits([p[1]])

    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = Init(p[1], p[3])

    def p_instruction_opt(self, p):
        """instructions_opt : instructions
                            | """
        if len(p) == 2:
            p[0] = InstructionsOpt(p[1])
        else:
            p[0] = InstructionsOpt([])

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            result = []
            result.extend(p[1].instructions)
            result.append(p[2])
            p[0] = Instructions(result)
        else:
            p[0] = Instructions([p[1]])

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expression ';'"""
        p[0] = PrintInstruction(p[2])

    def p_print_error_instr(self, p):
        """print_instr : PRINT error ';' """
        p[0] = PrintInstruction(p[2])

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = LabeledInstruction(p[1], p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AssignementInstr(p[1], p[3])

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction """
        if p[6] == 'else':
            p[0] = IfElseInstruction(p[3], p[5], p[7])
        else:
            p[0] = IfInstruction(p[3], p[5])

    def p_choice_error(self, p):
        """choice_instr : IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        p[0] = Error(p[3])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction """
        # todo: what does it mean error?
        p[0] = WhileInstruction(p[3], p[5])

    def p_while_error(self, p):
        """while_instr : WHILE '(' error ')' instruction """
        p[0] = Error(p[3])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = RepeatInstr(p[2], p[4])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = ReturnInstr(p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = ContinueInstr()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = BreakInstr()

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        p[0] = CompoundInstr(p[2], p[3])

    def p_condition(self, p):
        """condition : expression"""
        p[0] = Condition(p[1])

    def p_const_integer(self, p):
        """const : INTEGER"""
        p[0] = Integer(p[1])

    def p_const_float(self, p):
        """const : FLOAT"""
        p[0] = Float(p[1])

    def p_const_string(self, p):
        """const : STRING"""
        p[0] = String(p[1])

    def p_expression_const(self, p):
        """expression : const"""
        p[0] = ConstExpression(p[1])

    def p_expression_id(self, p):
        """expression : ID"""
        p[0] = IdExpression(p[1])

    def p_expression_mathop(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression"""
        if p[2] == '+':
            p[0] = AddExpression(p[1], p[3])
        elif p[2] == '-':
            p[0] = SubtractExpression(p[1], p[3])
        elif p[2] == '*':
            p[0] = MultiplyExpression(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivideExpression(p[1], p[3])
        elif p[2] == '%':
            p[0] = ModuloExpression(p[1], p[3])

    def p_expression_bitwise(self, p):
        """expression : expression '|' expression
                      | expression '&' expression
                      | expression '^' expression"""
        if p[2] == '|':
            p[0] = BinOrExpression(p[1], p[3])
        elif p[2] == '&':
            p[0] = BinAndExpression(p[1], p[3])
        elif p[2] == '^':
            p[0] = BinXorExpression(p[1], p[3])

    def p_expression_bool(self, p):
        """expression : expression AND expression
                      | expression OR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression"""
        if p[2] == '&&':
            p[0] = AndExpression(p[1], p[3])
        elif p[2] == '||':
            p[0] = OrExpression(p[1], p[3])
        elif p[2] == '==':
            p[0] = EqualExpression(p[1], p[3])
        elif p[2] == '!=':
            p[0] = NotEqualExpression(p[1], p[3])
        elif p[2] == '<':
            p[0] = LowerExpression(p[1], p[3])
        elif p[2] == '>':
            p[0] = GreaterExpression(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LowerEqualExpression(p[1], p[3])
        elif p[2] == '>=':
            p[0] = GreaterEqualExpression(p[1], p[3])

    def p_expression_bracket(self, p):
        """expression : '(' expression ')'"""
        p[0] = BracketExpression(p[2])

    def p_expression_error_bracket(self, p):
        """expression : '(' error ')'"""
        p[0] = Error(p[2])

    def p_funcall_expression(self, p):
        """expression : ID '(' expr_list_or_empty ')' """
        p[0] = FuncallExpression(p[1], p[3])

    def p_funcall_error(self, p):
        """expression : ID '(' error ')' """
        p[0] = Error(p[3])

    def p_shift_expression(self, p):
        """expression : expression SHL expression
                      | expression SHR expression"""
        if p[2] == '>>':
            p[0] = SHRExpression(p[1], p[3])
        elif p[2] == '<<':
            p[0] = SHLExpression(p[1], p[3])

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = ExpressionListOrEmpty(p[1])
        else:
            p[0] = Node()

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            result = []
            result.extend(p[1].expressions)
            result.append(p[3])
            p[0] = ExpressionList(result)
        else:
            p[0] = ExpressionList([p[1]])

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = FunDef(p[1], p[2], p[4], p[6])

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = ArgListOrEmpty(p[1])
        else:
            p[0] = ArgListOrEmpty([])

    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        if len(p) == 4:
            result = []
            result.extend(p[1].args)
            result.append(p[3])
            p[0] = ArgList(result)
        else:
            p[0] = ArgList([p[1]])

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = Argument(p[1], p[2])
