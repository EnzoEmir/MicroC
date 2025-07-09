#!/usr/bin/env python3
"""
Exemplo de uso da AST do MicroC
"""

from lark import Lark
from MicroC.ast import *
from MicroC.transformer import MicroCTransformer

# Código exemplo em MicroC
microc_code = """
int x;
int y;

int soma(int a, int b) {
    return a + b;
}

int main() {
    x = 10;
    y = 20;
    int resultado;
    resultado = soma(x, y);
    
    if (resultado > 25) {
        return 1;
    } else {
        return 0;
    }
}
"""

def main():
    # Carrega a gramática
    with open('MicroC/grammar.lark', 'r') as f:
        grammar = f.read()
    
    # Cria o parser
    parser = Lark(grammar, parser='lalr')
    
    # Faz o parse do código
    tree = parser.parse(microc_code)
    
    # Transforma em AST
    transformer = MicroCTransformer()
    ast = transformer.transform(tree)
    
    # Imprime a AST
    printer = ASTPrinter()
    print("AST do programa MicroC:")
    print("=" * 50)
    print(ast.accept(printer))
    
    # Exemplo de como visitar os nós da AST
    print("\n" + "=" * 50)
    print("Declarações no programa:")
    for decl in ast.declarations:
        if isinstance(decl, VarDecl):
            print(f"Variável: {decl.type} {decl.name}")
        elif isinstance(decl, FunDecl):
            print(f"Função: {decl.type} {decl.name}")
            print(f"  Parâmetros: {[f'{p.type} {p.name}' for p in decl.params]}")

if __name__ == "__main__":
    main()
