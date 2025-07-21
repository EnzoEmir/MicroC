import argparse

from . import eval as MicroC_eval

def make_argparser():
    parser = argparse.ArgumentParser(description="Compilador Lox")
    parser.add_argument(
        "file",
        help="Arquivo de entrada",
    )
    parser.add_argument(
        "-t",
        "--ast",
        action="store_true",
        help="Imprime a árvore sintática.",
    )
    parser.add_argument(
        "-l",
        "--lex",
        action="store_true",
        help="Imprime o lexer.",
    )
    parser.add_argument(
        "-c",
        "--cst",
        action="store_true",
        help="Imprime a árvore sintática concreta produzida pelo Lark.",
    )
    parser.add_argument(
        "-p",
        "--pm",
        action="store_true",
        help="Habilita o post-mortem debugger em caso de falha.",
    )
    parser.add_argument(
        "-s",
        "--sem",
        action="store_true",
        help="Executa a análise semântica.",
    )
    return parser

def main():
    parser = make_argparser()
    args = parser.parse_args()

    # Lê arquivo de entrada
    try:
        with open(args.file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Arquivo {args.file} não encontrado.")
        exit(1)

    # Imprime a árvore sintática concreta (CST) se solicitado
    if args.cst:
        from . import parser
        tree = parser.parse_source(source)
        if tree:
            print(tree.pretty())
        return

    # Imprime a árvore sintática abstrata (AST) se solicitado
    if args.ast:
        from . import parser
        from .transformer import MicroCTransformer
        tree = parser.parse_source(source)
        if tree:
            ast = MicroCTransformer().transform(tree)
            from .ast import ASTPrinter
            printer = ASTPrinter()
            print(ast.accept(printer))
        return

    # Imprime os tokens do lexer se solicitado
    if args.lex:
        from lark import Lark
        from . import parser as microc_parser
        # Reutiliza a gramática já carregada
        l = Lark(microc_parser.GRAMMAR, parser='lalr', lexer='standard')
        tokens = list(l.lex(source))
        for token in tokens:
            print(f"{token.type}: {token.value}")
        return
    
    # testa se a análise semântica está correta
    if args.sem:
        from . import parser
        from .transformer import MicroCTransformer
        from .semantic import SemanticAnalyzer # ou como for nomeado
        tree = parser.parse_source(source)
        if tree:
            ast = MicroCTransformer().transform(tree)
            analyzer = SemanticAnalyzer()
            try:
                analyzer.visit_program(ast)
                print("Análise semântica concluída com sucesso.")
            except Exception as e:
                print(f"Erro semântico: {e}")
        return

    if not args.ast and not args.cst and not args.lex and not args.sem:
        try:
            MicroC_eval(source)
        except Exception as e:
            on_error(e, args.pm)

def on_error(exception: Exception, pm: bool):
    if not pm:
        raise exception

    from ipdb import post_mortem  # type: ignore[import-untyped]

    post_mortem(exception.__traceback__)



    
if __name__ == "__main__":
    main()
