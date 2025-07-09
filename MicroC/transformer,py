from lark import Transformer

# Exemplo de esqueleto de transformer para MicroC
class MicroCTransformer(Transformer):
    def program(self, items):
        return ("program", items)

    def var_decl(self, items):
        return ("var_decl", items)

    def fun_decl(self, items):
        return ("fun_decl", items)

    def param(self, items):
        return ("param", items)

    def block(self, items):
        return ("block", items)

    def expr_stmt(self, items):
        return ("expr_stmt", items)

    def if_stmt(self, items):
        return ("if_stmt", items)

    def while_stmt(self, items):
        return ("while_stmt", items)

    def return_stmt(self, items):
        return ("return_stmt", items)

    def assignment(self, items):
        return ("assignment", items)

    def logic_or(self, items):
        return ("logic_or", items)

    def logic_and(self, items):
        return ("logic_and", items)

    def equality(self, items):
        return ("equality", items)

    def relational(self, items):
        return ("relational", items)

    def sum(self, items):
        return ("sum", items)

    def term(self, items):
        return ("term", items)

    def factor(self, items):
        return ("factor", items)

    def args(self, items):
        return ("args", items)

    def INT(self, token):
        return int(token)

    def ID(self, token):
        return str(token)
