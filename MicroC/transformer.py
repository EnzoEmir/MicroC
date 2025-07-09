from lark import Transformer, Token
from .ast import *


class MicroCTransformer(Transformer):
    """Transforma a árvore de parse do Lark em uma AST de MicroC."""
    
    def _convert_to_ast(self, item):
        """Converte um item primitivo para um objeto da AST."""
        if isinstance(item, int):
            return IntLiteral(item)
        elif isinstance(item, str):
            return Variable(item)
        elif isinstance(item, Token):
            if item.type == 'INT':
                return IntLiteral(int(item))
            elif item.type == 'ID':
                return Variable(str(item))
        return item  # Já é um objeto da AST
    
    def program(self, items):
        """program: (declaration)*"""
        return Program(items)
    
    def var_decl(self, items):
        """var_decl: type ID ";" """
        type_str, name = items
        if isinstance(name, Token):
            name = str(name)
        return VarDecl(type_str, name)
    
    def fun_decl(self, items):
        """fun_decl: type ID "(" params ")" block"""
        type_str, name, params, body = items
        if isinstance(name, Token):
            name = str(name)
        return FunDecl(type_str, name, params, body)
    
    def params(self, items):
        """params: (param ("," param)*)?"""
        return items if items else []
    
    def param(self, items):
        """param: type ID"""
        type_str, name = items
        if isinstance(name, Token):
            name = str(name)
        return Param(type_str, name)
    
    def type(self, items):
        """type: "int" | "void" """
        if items and len(items) > 0:
            item = items[0]
            if isinstance(item, Token):
                return str(item.value)
            return str(item)
        return "void"  # fallback
    
    def block(self, items):
        """block: "{" statement* "}" """
        return Block(items)
    
    def expr_stmt(self, items):
        """expr_stmt: expression ";" """
        expr = self._convert_to_ast(items[0])
        return ExprStmt(expr)
    
    def if_stmt(self, items):
        """if_stmt: "if" "(" expression ")" statement ("else" statement)?"""
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
        """while_stmt: "while" "(" expression ")" statement"""
        condition, body = items
        condition = self._convert_to_ast(condition)
        return WhileStmt(condition, body)
    
    def return_stmt(self, items):
        """return_stmt: "return" expression? ";" """
        if items:
            expr = self._convert_to_ast(items[0])
            return ReturnStmt(expr)
        return ReturnStmt()
    
    def assignment(self, items):
        """assignment: ID "=" assignment | logic_or"""
        if len(items) == 2:
            # É uma atribuição: ID = assignment
            name, value = items
            if isinstance(name, Token):
                name = str(name)
            
            # Converte valores primitivos para objetos da AST
            value = self._convert_to_ast(value)
            
            return Assignment(name, value)
        else:
            # É uma expressão logic_or
            return items[0]
    
    def logic_or(self, items):
        """logic_or: logic_and ("||" logic_and)*"""
        return self._create_binary_op(items, "||")
    
    def logic_and(self, items):
        """logic_and: equality ("&&" equality)*"""
        return self._create_binary_op(items, "&&")
    
    def equality(self, items):
        """equality: relational (("==" | "!=" ) relational)*"""
        return self._create_binary_op(items, ["==", "!="])
    
    def relational(self, items):
        """relational: sum (("<" | ">" | "<=" | ">=") sum)*"""
        return self._create_binary_op(items, ["<", ">", "<=", ">="])
    
    def sum(self, items):
        """sum: term (("+" | "-") term)*"""
        return self._create_binary_op(items, ["+", "-"])
    
    def term(self, items):
        """term: factor (("*" | "/") factor)*"""
        return self._create_binary_op(items, ["*", "/"])
    
    def factor(self, items):
        """factor: INT | ID | ID "(" [args] ")" | "(" expression ")" """
        if len(items) == 1:
            item = items[0]
            return self._convert_to_ast(item)
        elif len(items) == 2:
            # Chamada de função: ID args
            name, args = items
            if isinstance(name, Token):
                name = str(name)
            return FunctionCall(name, args)
        else:
            # Expressão entre parênteses já processada
            return items[0]
    
    def args(self, items):
        """args: expression ("," expression)*"""
        # Converte todos os argumentos para objetos da AST
        return [self._convert_to_ast(item) for item in items] if items else []
    
    def _create_binary_op(self, items, operators):
        """Cria operações binárias com associatividade à esquerda."""
        if len(items) == 1:
            return items[0]
        
        result = items[0]
        i = 1
        while i + 1 < len(items):
            operator = str(items[i])
            right = items[i + 1]
            # Converte operandos para objetos da AST se necessário
            result = self._convert_to_ast(result)
            right = self._convert_to_ast(right)
            result = BinaryOp(result, operator, right)
            i += 2
        
        return result
    
    def INT(self, token):
        """Terminal: literal inteiro"""
        return int(token)
    
    def ID(self, token):
        """Terminal: identificador"""
        return str(token)
