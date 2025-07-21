from .ast import *
from .erros import *
from .ctx import Environment

class SemanticAnalyzer(ASTVisitor):
    def __init__(self):
        self.env = Environment()  # escopo global
        self.functions = {}  # nome->(tipo_retorno, [tipos_param])
        self.current_return_type = None
        self.has_return = False

    def error(self, msg, token=None):
        raise SemanticError(msg, token)

    def visit_program(self, node):
        for decl in node.declarations:
            decl.accept(self)

    def visit_var_decl(self, node):
        if node.name in self.env.vars:
            self.error(f"Variável '{node.name}' já declarada.")
        self.env.set(node.name, node.type)
        if node.initializer:
            init_type = self.visit_expression(node.initializer)
            if init_type != node.type:
                self.error(f"Incompatibilidade de tipo em '{node.name}': esperado '{node.type}', recebeu '{init_type}'.")

    def visit_fun_decl(self, node):
        if node.name in self.functions:
            self.error(f"Função '{node.name}' já declarada.")
        param_types = [param.type for param in node.params]
        self.functions[node.name] = (node.type, param_types)

        prev_env = self.env
        self.env = Environment(prev_env)

        for param in node.params:
            self.env.set(param.name, param.type)

        prev_return = self.current_return_type
        prev_has_return = self.has_return

        self.current_return_type = node.type
        self.has_return = False

        node.body.accept(self)

        if self.current_return_type != "void" and not self.has_return:
            self.error(f"Função '{node.name}' deve conter ao menos um 'return' com valor.")

        self.current_return_type = prev_return
        self.has_return = prev_has_return
        self.env = prev_env

    def visit_param(self, node):
        pass

    def visit_block(self, node):
        prev_env = self.env
        self.env = Environment(prev_env)
        for stmt in node.statements:
            stmt.accept(self)
        self.env = prev_env

    def visit_expr_stmt(self, node):
        self.visit_expression(node.expression)

    def visit_if_stmt(self, node):
        cond_type = self.visit_expression(node.condition)
        if cond_type != "bool":
            self.error("Condição do if deve ser bool.")
        node.then_stmt.accept(self)
        if node.else_stmt:
            node.else_stmt.accept(self)

    def visit_while_stmt(self, node):
        cond_type = self.visit_expression(node.condition)
        if cond_type != "bool":
            self.error("Condição do while deve ser bool.")
        node.body.accept(self)

    def visit_return_stmt(self, node):
        self.has_return = True
        if node.expression:
            ret_type = self.visit_expression(node.expression)
            if ret_type != self.current_return_type:
                self.error(f"Tipo de retorno incompatível: esperado '{self.current_return_type}', recebeu '{ret_type}'.")
        else:
            if self.current_return_type != "void":
                self.error(f"Função do tipo '{self.current_return_type}' deve retornar valor.")

    def visit_assignment(self, node):
        try:
            var_type = self.env.get(node.name)
        except Exception:
            self.error(f"Variável '{node.name}' não declarada.")
        value_type = self.visit_expression(node.value)
        if var_type != value_type:
            self.error(f"Incompatibilidade de tipo na atribuição: '{var_type}' <- '{value_type}'.")

    def visit_binary_op(self, node):
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)
        op = node.operator
        if op in ['+', '-', '*', '/']:
            if left_type == right_type == "int":
                return "int"
            self.error("Operação aritmética requer inteiros.")
        if op in ['==', '!=', '<', '>', '<=', '>=']:
            if left_type == right_type == "int":
                return "bool"
            self.error("Operação relacional requer inteiros.")
        if op in ['&&', '||']:
            if left_type == right_type == "bool":
                return "bool"
            self.error("Operação lógica requer booleanos.")
        self.error(f"Operador '{op}' não suportado.")

    def visit_binaryop(self, node):
        return self.visit_binary_op(node)

    def visit_unary_op(self, node):
        operand_type = self.visit_expression(node.operand)
        op = node.operator
        if op == '!':
            if operand_type == "bool":
                return "bool"
            self.error("Operador '!' requer booleano.")
        if op in ['+', '-']:
            if operand_type == "int":
                return "int"
            self.error(f"Operador '{op}' requer inteiro.")
        self.error(f"Operador unário '{op}' não suportado.")

    def visit_functioncall(self, node):
        return self.visit_function_call(node)

    def visit_function_call(self, node):
        if node.name not in self.functions:
            self.error(f"Função '{node.name}' não declarada.")
        ret_type, param_types = self.functions[node.name]
        if len(node.args) != len(param_types):
            self.error(f"Função '{node.name}' espera {len(param_types)} argumentos, recebeu {len(node.args)}.")
        for arg, expected_type in zip(node.args, param_types):
            arg_type = self.visit_expression(arg)
            if arg_type != expected_type:
                self.error(f"Tipo de argumento incompatível em '{node.name}': esperado '{expected_type}', recebeu '{arg_type}'.")
        return ret_type

    def visit_print_call(self, node):
        return self.visit_expression(node.expression)

    def visit_variable(self, node):
        try:
            return self.env.get(node.name)
        except Exception:
            self.error(f"Variável '{node.name}' não declarada.")

    def visit_intliteral(self, node):
        return self.visit_int_literal(node)

    def visit_int_literal(self, node):
        return "int"

    def visit_boolliteral(self, node):
        return self.visit_bool_literal(node)

    def visit_bool_literal(self, node):
        return "bool"

    def visit_expression(self, node):
        # Tratamento especial para PrintCall que tem underscore no nome do método
        if isinstance(node, PrintCall):
            return self.visit_print_call(node)
        
        method = getattr(self, f"visit_{type(node).__name__.lower()}", None)
        if method:
            return method(node)
        self.error(f"Nó de expressão não suportado: {type(node).__name__}")
