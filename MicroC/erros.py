"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Exceções usadas no compilador MicroC.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ast import ASTNode


class SemanticError(Exception):
    """
    Exceção para erros semânticos.
    """

    def __init__(self, msg, token=None):
        super().__init__(msg)
        self.token = token


class ForceReturn(Exception):
    """
    Exceção que serve para forçar uma função a retornar durante a avaliação
    da mesma.
    """

    def __init__(self, value):
        self.value = value
        super().__init__(self.value)


class MicroCRuntimeError(Exception):
    """
    Exceção para erros de runtime específicos do MicroC.
    """
    
    def __init__(self, msg, token=None):
        super().__init__(msg)
        self.token = token


class UndefinedVariableError(SemanticError):
    """
    Exceção para quando uma variável não está definida.
    """
    
    def __init__(self, var_name, token=None):
        msg = f"Variável '{var_name}' não está definida."
        super().__init__(msg, token)
        self.var_name = var_name


class UndefinedFunctionError(SemanticError):
    """
    Exceção para quando uma função não está definida.
    """
    
    def __init__(self, func_name, token=None):
        msg = f"Função '{func_name}' não está definida."
        super().__init__(msg, token)
        self.func_name = func_name


class TypeMismatchError(SemanticError):
    """
    Exceção para incompatibilidades de tipo.
    """
    
    def __init__(self, expected, got, token=None):
        msg = f"Esperado tipo '{expected}', mas recebeu '{got}'."
        super().__init__(msg, token)
        self.expected = expected
        self.got = got


class ArgumentCountError(SemanticError):
    """
    Exceção para número incorreto de argumentos em chamada de função.
    """
    
    def __init__(self, func_name, expected, got, token=None):
        msg = f"Função '{func_name}' espera {expected} argumentos, mas recebeu {got}."
        super().__init__(msg, token)
        self.func_name = func_name
        self.expected = expected
        self.got = got
