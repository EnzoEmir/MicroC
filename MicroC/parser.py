from lark import Lark, UnexpectedInput
import os

# Caminho para o arquivo de gramática
GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), 'grammar.lark')

# Carrega a gramática do arquivo
with open(GRAMMAR_PATH, encoding='utf-8') as f:
    GRAMMAR = f.read()

# Cria o parser Lark
parser = Lark(GRAMMAR, parser='lalr', start='start', propagate_positions=True)

def parse_source(source: str):
    """
    Faz o parsing do código-fonte de MicroC e retorna a árvore sintática concreta (CST).
    """
    try:
        tree = parser.parse(source)
        return tree
    except UnexpectedInput as e:
        print('Erro de sintaxe:', e)
        return None
