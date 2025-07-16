from lark import Transformer, Token
from .ast import *


class MicroCTransformer(Transformer):
    def NOT(self, token):
        return str(token)
    def BOOL(self, token):
        # token é 'true' ou 'false'
        return BoolLiteral(token == 'true')
    # Métodos para preservar os operadores como strings na AST
    def PLUS(self, token):
        return str(token)

    def MINUS(self, token):
        return str(token)

    def TIMES(self, token):
        return str(token)

    def DIVIDE(self, token):
        return str(token)

    def EQ(self, token):
        return str(token)

    def NE(self, token):
        return str(token)

    def LT(self, token):
        return str(token)

    def GT(self, token):
        return str(token)

    def LE(self, token):
        return str(token)

    def GE(self, token):
        return str(token)

    def OR(self, token):
        return str(token)

    def AND(self, token):
        return str(token)
    """Transforma a árvore de parse do Lark em uma AST de MicroC."""
    
    def _convert_to_ast(self, item):
        """Converte um item primitivo para um objeto da AST."""
        # Se já for um nó da AST, retorna direto
        if isinstance(item, (ASTNode, list)):
            return item
        if isinstance(item, int):
            return IntLiteral(item)
        elif isinstance(item, str):
            if item == 'true':
                return BoolLiteral(True)
            elif item == 'false':
                return BoolLiteral(False)
            return Variable(item)
        elif isinstance(item, Token):
            if item.type == 'INT':
                return IntLiteral(int(item))
            elif item.type == 'BOOL':
                return BoolLiteral(str(item) == 'true')
            elif item.type == 'ID':
                return Variable(str(item))
        return item
    
    def program(self, items):
        return Program(items)
    
    def var_decl(self, items):
        # type_str, name = items
        # if isinstance(name, Token):
        #     name = str(name)
        # return VarDecl(type_str, name)
        # print("items", items)
        type_str = items[0]
        name = items[1]
        if isinstance(name, Token):
            name = str(name)

        initializer = items[2] if len(items) > 2 else None
        return VarDecl(type_str, name, initializer)
    
    def fun_decl(self, items):
        type_str, name, params, body = items
        if isinstance(name, Token):
            name = str(name)
        return FunDecl(type_str, name, params, body)
    
    def params(self, items):
        return items if items else []
    
    def param(self, items):
        type_str, name = items
        if isinstance(name, Token):
            name = str(name)
        return Param(type_str, name)
    
    def type(self, items):
        if items and len(items) > 0:
            item = items[0]
            if isinstance(item, Token):
                return str(item.value)
            return str(item)
        print("Valor não reconhecido ou ausente em type")
        return "void"  # fallback
    
    def block(self, items):
        return Block(items)
    
    def expr_stmt(self, items):
        # print("expr_stmt", items)
        # print()
        expr = self._convert_to_ast(items[0])
        return ExprStmt(expr)
    
    def if_stmt(self, items):
        if len(items) == 2:
            # Sem else
            condition, then_stmt = items
            condition = self._convert_to_ast(condition)
            return IfStmt(condition, then_stmt)
        else:
            # Com else
            condition, then_stmt, else_stmt = items
            condition = self._convert_to_ast(condition)
            return IfStmt(condition, then_stmt, else_stmt)
    
    def while_stmt(self, items):
        condition, body = items
        condition = self._convert_to_ast(condition)
        return WhileStmt(condition, body)
    
    def return_stmt(self, items):
        if items:
            expr = self._convert_to_ast(items[0])
            return ReturnStmt(expr)
        return ReturnStmt()
    
    def assignment(self, items):
        if len(items) == 2:
            # É uma atribuição: ID = assignment
            name, value = items
            if isinstance(name, Token):
                name = str(name)
            # O lado direito pode ser uma lista se for uma chamada de função mal processada
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            value = self._convert_to_ast(value)
            return Assignment(name, value)
        else:
            # É uma expressão logic_or
            expr = items[0]
            if isinstance(expr, list) and len(expr) == 1:
                expr = expr[0]
            return expr
    
    def logic_or(self, items):
        return self._create_binary_op(items, "||")
    
    def logic_and(self, items):
        return self._create_binary_op(items, "&&")
    
    def equality(self, items):
        return self._create_binary_op(items, ["==", "!="])
    
    def relational(self, items):
        # return self._create_binary_op(items, ["<", ">", "<=", ">="])
        if len(items) == 1:
            return items[0]
        # Para casos como x > 5, items = [x, '>', 5]
        result = self._convert_to_ast(items[0])
        i = 1
        while i + 1 < len(items):
            op = items[i]
            right = self._convert_to_ast(items[i + 1])
            result = BinaryOp(result, op, right)
            i += 2
        return result
        
    def sum(self, items):
        return self._create_binary_op(items, ["+", "-"])
    
    def term(self, items):
        return self._create_binary_op(items, ["*", "/"])
    
    def factor(self, items):
        # print("estou factor", items)
        # print()
        if len(items) == 1:
            item = items[0]
            result = self._convert_to_ast(item)
            return result
        elif len(items) == 2:
            # Pode ser negação (!factor) ou chamada de função (ID args)
            if items[0] == '!':
                operand = self._convert_to_ast(items[1])
                return UnaryOp('!', operand)
            else:
                # Chamada de função: ID args
                name, args = items
                if isinstance(name, Token):
                    name = str(name)
                result = FunctionCall(name, args)
                return result
        else:
            # Expressão entre parênteses já processada
            return items[0]
        
    def fun_call(self, items):
        # print("items do fun_call", items)
        name = str(items[0])
        args = items[1] if len(items) > 1 else []
        return FunctionCall(name=name, args=args)
    
    def print_call(self, items):
        # print("items do print_call", items)
        expression = self._convert_to_ast(items[0])
        return PrintCall(expression=expression)
        
    
    def args(self, items):
        # Converte todos os argumentos para objetos da AST
        result = [self._convert_to_ast(item) for item in items] if items else []
        return result
    
    def _create_binary_op(self, items, operators):
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            # Caso simples: a + b
            left = self._convert_to_ast(items[0])
            right = self._convert_to_ast(items[1])
            op = operators[0] if isinstance(operators, str) else operators[0]
            result = BinaryOp(left, op, right)
            return result
        result = self._convert_to_ast(items[0])
        i = 1
        while i + 1 < len(items):
            operator = str(items[i])
            right = items[i + 1]
            right = self._convert_to_ast(right)
            result = BinaryOp(result, operator, right)
            i += 2
        return result
    
    def INT(self, token):
        return int(token)

    def ID(self, token):
        return str(token)
