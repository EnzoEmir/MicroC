"""
AST (Abstract Syntax Tree) para o projeto MicroC

Este módulo define as classes que representam os nós da árvore sintática abstrata
para a linguagem MicroC, baseada na gramática definida em grammar.lark.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
from dataclasses import dataclass


class ASTNode(ABC):
    """Classe base para todos os nós da AST."""
    
    @abstractmethod
    def accept(self, visitor):
        """Método para implementar o padrão Visitor."""
        pass


# ==================== PROGRAMA E DECLARAÇÕES ====================

@dataclass
class Program(ASTNode):
    """Nó raiz do programa - contém todas as declarações."""
    declarations: List['Declaration']
    
    def accept(self, visitor):
        return visitor.visit_program(self)



class Declaration(ASTNode):
    """Classe base para declarações."""
    pass


@dataclass
class VarDecl(Declaration):
    """Declaração de variável: tipo nome;"""
    type: str
    name: str
    initializer: Optional[ASTNode] = None  
    
    def accept(self, visitor):
        return visitor.visit_var_decl(self)


@dataclass
class FunDecl(Declaration):
    """Declaração de função: tipo nome(params) { body }"""
    type: str
    name: str
    params: List['Param']
    body: 'Block'
    
    def accept(self, visitor):
        return visitor.visit_fun_decl(self)


@dataclass
class Param(ASTNode):
    """Parâmetro de função: tipo nome"""
    type: str
    name: str
    
    def accept(self, visitor):
        return visitor.visit_param(self)


# ==================== STATEMENTS ====================


class Statement(ASTNode):
    """Classe base para statements."""
    pass


@dataclass
class Block(Statement):
    """Bloco de código: { statements }"""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_block(self)


@dataclass
class ExprStmt(Statement):
    """Statement de expressão: expression;"""
    expression: 'Expression'
    
    def accept(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class IfStmt(Statement):
    """Statement if: if (condition) then_stmt [else else_stmt]"""
    condition: 'Expression'
    then_stmt: Statement
    else_stmt: Optional[Statement] = None
    
    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


@dataclass
class WhileStmt(Statement):
    """Statement while: while (condition) body"""
    condition: 'Expression'
    body: Statement
    
    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


@dataclass
class ReturnStmt(Statement):
    """Statement return: return [expression];"""
    expression: Optional['Expression'] = None
    
    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


# ==================== EXPRESSIONS ====================


class Expression(ASTNode):
    """Classe base para expressões."""
    pass


@dataclass
class Assignment(Expression):
    """Expressão de atribuição: id = expression"""
    name: str
    value: Expression
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)


@dataclass
class BinaryOp(Expression):
    """Expressão binária: left op right"""
    left: Expression
    operator: str
    right: Expression
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(Expression):
    """Expressão unária: op operand"""
    operator: str
    operand: Expression
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)


@dataclass
class FunctionCall(Expression):
    """Chamada de função: name(args)"""
    name: str
    args: List[Expression]
    
    def accept(self, visitor):
        return visitor.visit_function_call(self)


@dataclass
class PrintCall(Expression):
    """Chamada de print: print(expression)"""
    expression: Expression
    
    def accept(self, visitor):
        return visitor.visit_print_call(self)


@dataclass
class Variable(Expression):
    """Referência a variável: id"""
    name: str
    
    def accept(self, visitor):
        return visitor.visit_variable(self)



@dataclass
class IntLiteral(Expression):
    """Literal inteiro: 42"""
    value: int
    
    def accept(self, visitor):
        return visitor.visit_int_literal(self)

@dataclass
class BoolLiteral(Expression):
    """Literal booleano: true/false"""
    value: bool

    def accept(self, visitor):
        return visitor.visit_bool_literal(self)


# ==================== VISITOR PATTERN ====================

class ASTVisitor(ABC):
    """Interface para visitantes da AST."""
    
    @abstractmethod
    def visit_program(self, node: Program): pass
    
    @abstractmethod
    def visit_var_decl(self, node: VarDecl): pass
    
    @abstractmethod
    def visit_fun_decl(self, node: FunDecl): pass
    
    @abstractmethod
    def visit_param(self, node: Param): pass
    
    @abstractmethod
    def visit_block(self, node: Block): pass
    
    @abstractmethod
    def visit_expr_stmt(self, node: ExprStmt): pass
    
    @abstractmethod
    def visit_if_stmt(self, node: IfStmt): pass
    
    @abstractmethod
    def visit_while_stmt(self, node: WhileStmt): pass
    
    @abstractmethod
    def visit_return_stmt(self, node: ReturnStmt): pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment): pass
    
    @abstractmethod
    def visit_binary_op(self, node: BinaryOp): pass
    
    @abstractmethod
    def visit_unary_op(self, node: UnaryOp): pass
    
    @abstractmethod
    def visit_function_call(self, node: FunctionCall): pass
    
    @abstractmethod
    def visit_print_call(self, node: PrintCall): pass
    
    @abstractmethod
    def visit_variable(self, node: Variable): pass
    
    @abstractmethod
    def visit_int_literal(self, node: IntLiteral): pass

    @abstractmethod
    def visit_bool_literal(self, node: BoolLiteral): pass


# ==================== UTILITÁRIOS ====================
class ASTPrinter(ASTVisitor):
    def visit_bool_literal(self, node):
        return f"BoolLiteral({str(node.value).lower()})"
    """Visitor para imprimir a AST de forma legível."""
    def __init__(self):
        self.indent_level = 0

    def _indent(self):
        return "  " * self.indent_level

    def visit_program(self, node: Program):
        result = "Program:\n"
        self.indent_level += 1
        for decl in node.declarations:
            result += self._indent() + str(decl.accept(self)) + "\n"
        self.indent_level -= 1
        return result.rstrip()

    def visit_var_decl(self, node: VarDecl):
        return f"VarDecl({node.type} {node.name})"

    def visit_fun_decl(self, node: FunDecl):
        params_str = ", ".join([param.accept(self) for param in node.params])
        result = f"FunDecl({node.type} {node.name}({params_str}))"
        self.indent_level += 1
        result += "\n" + self._indent() + node.body.accept(self)
        self.indent_level -= 1
        return result

    def visit_param(self, node: Param):
        return f"{node.type} {node.name}"

    def visit_block(self, node: Block):
        result = "Block:"
        self.indent_level += 1
        for stmt in node.statements:
            result += "\n" + self._indent() + str(stmt.accept(self))
        self.indent_level -= 1
        return result

    def visit_expr_stmt(self, node: ExprStmt):
        return f"ExprStmt({node.expression.accept(self)})"

    def visit_if_stmt(self, node: IfStmt):
        result = f"IfStmt({node.condition.accept(self)})"
        self.indent_level += 1
        result += "\n" + self._indent() + "Then: " + node.then_stmt.accept(self)
        if node.else_stmt:
            result += "\n" + self._indent() + "Else: " + node.else_stmt.accept(self)
        self.indent_level -= 1
        return result

    def visit_while_stmt(self, node: WhileStmt):
        result = f"WhileStmt({node.condition.accept(self)})"
        self.indent_level += 1
        result += "\n" + self._indent() + node.body.accept(self)
        self.indent_level -= 1
        return result

    def visit_return_stmt(self, node: ReturnStmt):
        if node.expression:
            return f"ReturnStmt({node.expression.accept(self)})"
        return "ReturnStmt()"

    def visit_assignment(self, node: Assignment):
        return f"Assignment({node.name} = {node.value.accept(self)})"

    def visit_binary_op(self, node: BinaryOp):
        return f"BinaryOp({node.left.accept(self)} {node.operator} {node.right.accept(self)})"

    def visit_unary_op(self, node: UnaryOp):
        return f"UnaryOp({node.operator} {node.operand.accept(self)})"

    def visit_function_call(self, node: FunctionCall):
        args_str = ", ".join([arg.accept(self) for arg in node.args])
        return f"FunctionCall({node.name}({args_str}))"
    
    def visit_print_call(self, node: PrintCall):
        return f"PrintCall({node.expression.accept(self)})"

    def visit_variable(self, node: Variable):
        return f"Variable({node.name})"

    def visit_int_literal(self, node: IntLiteral):
        return f"IntLiteral({node.value})"