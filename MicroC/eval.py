from .ast import *
from .ctx import *
from .erros import *

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter(ASTVisitor):
    def visit_bool_literal(self, node):
        return node.value
    def __init__(self, program):
        self.program = program

        self.env = Environment() #nosso contexto, vem de ctx

        self.functions = {}
        self._register_functions(program)

    def _register_functions(self, program):
        for decl in program.declarations:
            if isinstance(decl, FunDecl):
                self.functions[decl.name] = decl
            elif isinstance(decl, VarDecl):
                # Avalia o inicializador se existir
                if decl.initializer is not None:
                    # Precisamos usar um interpretador temporário para avaliar
                    value = decl.initializer.accept(self) if hasattr(decl.initializer, 'accept') else decl.initializer
                else:
                    value = 0
                self.env.set(decl.name, value)

    def run(self):
        if 'main' not in self.functions:
            raise UndefinedFunctionError('main')
        # Ao chamar main, use o ambiente global diretamente
        func = self.functions['main']
        try:
            result = self._eval_block(func.body, self.env)
        except ReturnValue as rv:
            result = rv.value
        return result

    def _call_function(self, name, args):
        func = self.functions.get(name)
        if not func:
            raise UndefinedFunctionError(name)
        
        # Verifica se o número de argumentos está correto
        if len(args) != len(func.params):
            raise ArgumentCountError(name, len(func.params), len(args))
            
        local_env = Environment(self.env)
        for param, arg in zip(func.params, args):
            local_env.set(param.name, arg)
        try:
            result = self._eval_block(func.body, local_env)
            return result
        except ReturnValue as rv:
            return rv.value

    def _eval_block(self, block, env):
        prev_env = self.env
        self.env = env
        try:
            for stmt in block.statements:
                stmt.accept(self)
        except ReturnValue as rv:
            raise rv  # Propaga para cima
        finally:
            self.env = prev_env

    def visit_program(self, node):
        # Executa comandos e declarações globais (ex: global = 5;)
        for decl in node.declarations:
            if isinstance(decl, FunDecl):
                self.functions[decl.name] = decl
            elif isinstance(decl, VarDecl):
                value = decl.initializer if decl.initializer is not None else 0
                self.env.set(decl.name, value)
            else:
                decl.accept(self)

        return self.run()

    def visit_var_decl(self, node):
        # Avalia o inicializador se existir
        if node.initializer is not None:
            value = node.initializer.accept(self)
        else:
            value = 0  # valor padrão
        self.env.set(node.name, value)

    def visit_fun_decl(self, node):
        pass  # já registrado

    def visit_param(self, node):
        pass

    def visit_block(self, node):
        # Só cria novo escopo se não for o corpo de uma função
        new_env = Environment(self.env)

        # Se o escopo atual já é de função (ou global), apenas executa no escopo atual
        # self._eval_block(node, new_env)
        try:
            self._eval_block(node, new_env)
        except ReturnValue as rv:
            # Propaga o retorno para cima
            raise rv

    def visit_expr_stmt(self, node):
        node.expression.accept(self)

    def visit_if_stmt(self, node):
        cond = node.condition.accept(self)
        if cond:
            node.then_stmt.accept(self)
        elif node.else_stmt:
            node.else_stmt.accept(self)

    def visit_while_stmt(self, node):
        while node.condition.accept(self):
            node.body.accept(self)

    def visit_return_stmt(self, node):
        value = node.expression.accept(self) if node.expression else 0
        raise ReturnValue(value)

    def visit_assignment(self, node):
        value = node.value.accept(self)
        self.env.update(node.name, value)
        return value

    def visit_binary_op(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        op = node.operator
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left // right
        if op == '==': return int(left == right)
        if op == '!=': return int(left != right)
        if op == '<': return int(left < right)
        if op == '>': return int(left > right)
        if op == '<=': return int(left <= right)
        if op == '>=': return int(left >= right)
        if op == '&&': return int(bool(left) and bool(right))
        if op == '||': return int(bool(left) or bool(right))
        raise Exception(f"Operador binário não suportado: {op}")

    def visit_unary_op(self, node):
        operand = node.operand.accept(self)
        op = node.operator
        if op == '-':
            return -operand
        if op == '+':
            return +operand
        if op == '!':
            # Considera 0/False como False, qualquer outro valor como True
            return int(not bool(operand))
        raise Exception(f"Operador unário não suportado: {op}")

    def visit_function_call(self, node):
        args = [arg.accept(self) for arg in node.args]
        return self._call_function(node.name, args)
    
    def visit_print_call(self, node):
        value = node.expression.accept(self)
        print(value)
        return value  # print retorna o valor impresso

    def visit_variable(self, node):
        value = self.env.get(node.name)

        # Se o valor ainda for um nó da AST (não avaliado), avalia ele
        while hasattr(value, "accept"):
            value = value.accept(self)

        return value

    def visit_int_literal(self, node):
        return node.value

def eval(source):
    from .parser import parse_source
    from .transformer import MicroCTransformer
    from .semantic import SemanticAnalyzer

    tree = parse_source(source)
    if not tree:
        raise Exception("Erro de sintaxe.")
    
    ast = MicroCTransformer().transform(tree)

    #testando semântica
    analyzer = SemanticAnalyzer()
    try:
        analyzer.visit_program(ast)
    except Exception as e:
        print(f"Erro semântico: {e}")

    interpreter = Interpreter(ast)

    result = interpreter.visit_program(ast)

    print(result)
    return result
