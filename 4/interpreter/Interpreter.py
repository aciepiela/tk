# -*- coding: utf-8 -*-

from ast.AST import *
from interpreter.Memory import *
from interpreter.Exceptions import *
from interpreter.visit import *

operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,

    '^': lambda x, y: x ^ y,
    '|': lambda x, y: x | y,
    '&': lambda x, y: x & y,
    'SHL': lambda x, y: x << y,
    'SHR': lambda x, y: x >> y,

    'OR': lambda x, y: x or y,
    'AND': lambda x, y: x and y,
    '<=': lambda x, y: not (x > y),
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: not x == y
}


class Interpreter(object):
    def __init__(self):
        self.memoryStack = MemoryStack()
        self.functions = FunctionMemory()

    @on('node')
    def visit(self, node):
        print "visit", node

    def count_or_get_value_from_memory(self, node):
        if isinstance(node, str):
            return self.memoryStack.get(node)
        else:
            return node.accept_interpreter(self)

    def fill_memory(self, memory, declarations):
        for declaration in declarations:
            for var in declaration.variables:
                initial_value = self.count_or_get_value_from_memory(var.right)
                memory.put(var.left, initial_value)

    def interpret_instruction_block(self, block):
        if isinstance(block, list):
            for instr in block:
                instr.accept_interpreter(self)
        elif isinstance(block, Node):
            block.accept_interpreter(self)

    def interpret_parts(self, parts, global_memory):
        for p in parts:
            if isinstance(p, Declaration):
                self.fill_memory(global_memory, p)
                self.memoryStack = MemoryStack(global_memory)
                self.functions.pushGlobalMemory(global_memory)
            if isinstance(p, Variable):
                for var in p.variables:
                    initial_value = self.count_or_get_value_from_memory(var.right)
                    global_memory.put(var.left, initial_value)
                    self.memoryStack = MemoryStack(global_memory)
                    self.functions.pushGlobalMemory(global_memory)
            elif isinstance(p, FunctionDefinition):
                p.accept_interpreter(self)
            elif isinstance(p, CompoundInstruction):
                self.interpret_instruction_block(p)
            else:
                p.accept_interpreter(self)

    @when(Program)
    def visit(self, node):
        global_memory = Memory("program stack")
        self.interpret_parts(node.part, global_memory)

    @when(FunctionDefinition)
    def visit(self, node):
        memory = Memory("arguments of " + node.ident)
        for arg in node.args:
            memory.put(arg.ident, None)

        self.functions.putFunction(node.ident, memory, node)

    @when(FunctionCall)
    def visit(self, node):
        fundef = self.functions.getFunction(node.ident)

        args = node.args
        memory = Memory("funcall")
        for def_arg, passed_arg in zip(fundef.args, args):
            memory.put(def_arg.ident, self.count_or_get_value_from_memory(passed_arg))

        previous_stack = self.memoryStack
        self.memoryStack = self.functions.getStack(node.ident, memory)
        try:
            fundef.instr.accept_interpreter(self)
        except ReturnException as ret:
            self.memoryStack = previous_stack
            return ret.value

        self.memoryStack = previous_stack

    @when(WhileLoop)
    def visit(self, node):
        try:
            while node.cond.accept_interpreter(self):
                try:
                    node.instr.accept_interpreter(self)
                except ContinueException:
                    pass
        except BreakException:
            pass

    @when(RepeatUntilLoop)
    def visit(self, node):
        try:
            while True:
                try:
                    for i in node.instr:
                        i.accept_interpreter(self)
                except ContinueException:
                    pass
                if node.cond.accept_interpreter(self):
                    break
        except BreakException:
            pass

    @when(CompoundInstruction)
    def visit(self, node):
        memory = Memory("compInstr(" + str(node.lineno) + ") scope")
        self.fill_memory(memory, node.decl)
        self.memoryStack.push(memory)
        self.interpret_instruction_block(node.instr)
        return self.memoryStack.pop()

    @when(Break)
    def visit(self, node):
        raise BreakException()

    @when(Continue)
    def visit(self, node):
        raise ContinueException()

    @when(Print)
    def visit(self, node):
        print self.count_or_get_value_from_memory(node.expr)

    @when(Return)
    def visit(self, node):
        value = self.count_or_get_value_from_memory(node.value)
        raise ReturnException(value)

    @when(RelExpr)
    def visit(self, node):
        r1 = self.count_or_get_value_from_memory(node.left)
        r2 = self.count_or_get_value_from_memory(node.right)
        result = operators[node.op](r1, r2)
        if not isinstance(result, bool):
            raise Exception("not bool operator: " + node.op + " in line " + node.lineno)
        return result

    @when(BinExpr)
    def visit(self, node):
        r1 = self.count_or_get_value_from_memory(node.left)
        r2 = self.count_or_get_value_from_memory(node.right)
        result = operators[node.op](r1, r2)
        return result

    @when(Assignment)
    def visit(self, node):
        varName = node.left
        value = self.count_or_get_value_from_memory(node.right)
        self.memoryStack.put(varName, value)

    @when(Const)
    def visit(self, node):
        return node.value

    @when(ChoiceInstruction)
    def visit(self, node):
        if node.cond.accept_interpreter(self):
            node.instr.accept_interpreter(self)

    @when(ChoiceInstructionWithElse)
    def visit(self, node):
        if node.cond.accept_interpreter(self):
            node.instr.accept_interpreter(self)
        else:
            node.elinstr.accept_interpreter(self)