# Interpretador MicroC

## Integrantes

| Nome | Matrícula | Turma |
|------|-----------|-------|
| Caio Venâncio do Rosário | [231027195] | [T02] |
| Enzo Emir Viana Ferraz | [231011293] | [T02] |
| Marcelo Makoto Araki Takechi | [231026465] | [T02] |

## Introdução

O **MicroC** é um interpretador para uma versão simplificada da linguagem C, desenvolvido como projeto final da disciplina de Compiladores do primeiro semestre de 2025. O projeto implementa as principais etapas de um compilador moderno, desde a análise léxica até a interpretação do código.

### Estratégias e Algoritmos Implementados

O interpretador foi desenvolvido utilizando as seguintes estratégias:

1. **Análise Léxica e Sintática**: Implementada utilizando a biblioteca Lark, que gera automaticamente um parser LALR a partir de uma gramática BNF.

2. **Árvore Sintática Abstrata (AST)**: Utiliza o padrão Visitor para percorrer e processar a AST, facilitando a separação entre a estrutura dos dados e as operações realizadas sobre eles.

3. **Ambiente de Execução**: Implementa um sistema de escopos encadeados para gerenciar variáveis locais e globais, permitindo shadowing correto de variáveis.

4. **Interpretação Direta**: O código é executado diretamente a partir da AST, sem geração de código intermediário.

### Sintaxe e Semântica da Linguagem

O MicroC suporta um subconjunto da linguagem C com as seguintes características:

#### Tipos de Dados
```c
int x = 42;        // Números inteiros
bool flag = true;  // Valores booleanos (true/false)
void func() { }    // Tipo vazio para funções
```

#### Estruturas de Controle
```c
// Condicionais
if (x > 10) {
    print(x);
} else {
    print(0);
}

// Loops
while (i < 10) {
    i = i + 1;
}
```

#### Funções
```c
int soma(int a, int b) {
    return a + b;
}

int main() {
    int resultado = soma(5, 3);
    return resultado;
}
```

#### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`
- **Relacionais**: `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Lógicos**: `&&`, `||`, `!`

## Status de Implementação

| Etapa | Status | Descrição |
|-------|--------|-----------|
| **Análise Léxica** | ✅ | Tokenização usando Lark |
| **Análise Sintática** | ✅ | Construção da AST |
| **Análise Semântica** | ✅ | Verificação completa de tipos e escopos |
| **Interpretação** | ✅ | Execução via visitor pattern |

## Instalação

### Pré-requisitos
- Python 3.10 ou superior
- UV (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/EnzoEmir/MicroC.git
   cd MicroC
   ```

2. Certifique-se de estar no diretório raiz do projeto (onde está a pasta `MicroC/`)

3. Instale o `uv`:
   ```bash
   pip install uv
   ```
4. Para baixar as dependencias do projeto
```bash
uv run MicroC
```
### Execução

#### Execução Básica
```bash
uv run MicroC arquivo.mc
```

#### Opções de Debug
| Comando | Descrição |
|---------|-----------|
| `uv run MicroC programa.mc` | Execução normal |
| `uv run MicroC -l programa.mc` | Mostra tokens do lexer |
| `uv run MicroC -c programa.mc` | Mostra árvore sintática concreta (CST) |
| `uv run MicroC -t programa.mc` | Mostra árvore sintática abstrata (AST) |
| `uv run MicroC -p programa.mc` | Habilita debugger em caso de erro |
| `uv run MicroC -s programa.mc` | Realiza análise semântica sobre o código |

> **Nota**: O interpretador aceita arquivos com qualquer extensão. A extensão `.mc` é apenas uma convenção sugerida.


## Como Usar

### Pré-requisitos
1. Certifique-se de estar no diretório raiz do projeto (onde está a pasta `MicroC/`)
2. Instale o `uv`:
   ```bash
   pip install uv
   ```
3. Para baixar as dependencias do projeto
```bash
uv run MicroC
```
## Exemplos de Uso

### Exemplo 1: Programa Básico com Variáveis
**Arquivo:** `examples/var_decl.mc`
```c
/* Declaração e inicialização de variáveis */
int x = 10;
int y = 20;

int main() {
    int z = x + y;
    print(z);
    return z;
}
```

**Execução:**
```bash
uv run MicroC examples/var_decl.mc
```

**Saída esperada:**
```
30
```

### Exemplo 2: Função com Parâmetros
**Arquivo:** `examples/example_soma3.mc`
```c
/* Função que calcula a soma de três números */
int soma3(int a, int b, int c) {
    return a + b + c;
}

int main() {
    int resultado = soma3(1, 2, 3);
    print(resultado);
    return 0;
}
```

**Execução:**
```bash
uv run MicroC examples/example_soma3.mc
```

**Saída esperada:**
```
6
```

### Exemplo 3: Estruturas de Controle
**Arquivo:** `examples/escopo_if.mc`
```c
int main() {
    int x = 15;
    
    if (x > 10) {
        int y = x * 2;
        print(y);
    } else {
        print(x);
    }
    
    return x;
}
```

**Execução:**
```bash
uv run MicroC examples/escopo_if.mc
```

**Saída esperada:**
```
30
```

### Exemplo 4: Escopo de Variáveis
**Arquivo:** `examples/escopo_funcao.mc`
```c
int global_var = 100;

int test_func() {
    int local_var = 50;
    return global_var + local_var;
}

int main() {
    int resultado = test_func();
    print(resultado);
    return 0;
}
```

**Execução:**
```bash
uv run MicroC examples/escopo_funcao.mc
```

**Saída esperada:**
```
150
```

## Referências

### Bibliografia Técnica
- **Microsoft Learn** - Documentação da Linguagem C
  - URL: https://learn.microsoft.com/pt-br/cpp/c-language/?view=msvc-170

### Ferramentas e Bibliotecas
- **Lark Parser** - Framework de parsing para Python
  - Documentação: https://lark-parser.readthedocs.io/
  - Repositório: https://github.com/lark-parser/lark

### Padrões de Projeto Utilizados
- **Visitor Pattern** - Para traversal da AST
- **Transformer Pattern** - Para conversão de parse tree para AST

### Créditos
  Algumas práticas e referências deste código foram tiradas do repositório do interpretador Lox feito durante a disciplina.
- **Repositório do interpretador Lox:** https://github.com/fabiommendes/lox-base

## Estrutura do Código

### Organização dos Módulos

```
MicroC/
├── __init__.py          # Inicialização do pacote
├── __main__.py          # Ponto de entrada da aplicação
├── ast.py               # Definição dos nós da AST
├── ctx.py               # Gerenciamento de contexto/escopo
├── erros.py             # Classes de erro customizadas
├── eval.py              # Interpretador (visitor da AST)
├── grammar.lark         # Gramática da linguagem MicroC
├── parser.py            # Parser baseado em Lark
├── semantic.py          # Análise semântica completa
└── transformer.py       # Transformação parse tree → AST
```

### Principais Classes e Responsabilidades

#### `ast.py` - Abstract Syntax Tree
- **`ASTNode`**: Classe base para todos os nós da AST
- **`ASTVisitor`**: Interface para implementação do padrão Visitor
- **Nós de Expressão**: `BinaryOp`, `UnaryOp`, `FunCall`, `Identifier`, `Literal`
- **Nós de Declaração**: `VarDecl`, `FunDecl`, `Program`
- **Nós de Comando**: `Assignment`, `If`, `While`, `Return`, `Block`, `PrintCall`

#### `transformer.py` - Conversão Parse Tree → AST
- **`MicroCTransformer`**: Converte árvore de parsing do Lark em AST
- **`_convert_to_ast()`**: Função auxiliar para conversão de tipos

#### `eval.py` - Interpretador
- **`Interpreter`**: Executa a AST usando padrão Visitor
- **`visit_*`**: Métodos para cada tipo de nó da AST
- **Gerenciamento de escopo**: Integração com `Environment`

#### `ctx.py` - Contexto e Escopo
- **`Environment`**: Gerencia variáveis e escopos
- **Escopo hierárquico**: Suporte a escopos aninhados (global, função, bloco)

#### `parser.py` - Análise Sintática
- **`MicroCParser`**: Interface para o parser Lark
- **Integração**: Combina gramática + transformer

### Fluxo de Execução

1. **Análise Léxica/Sintática**: `parser.py` + `grammar.lark`
   ```
   Código fonte → Tokens → Parse Tree
   ```

2. **Transformação**: `transformer.py`
   ```
   Parse Tree → AST
   ```

3. **Interpretação**: `eval.py`
   ```
   AST → Execução (usando Visitor Pattern)
   ```

### Arquitetura do Visitor Pattern

```python
class ASTVisitor:
    def visit(self, node: ASTNode) -> Any:
        """Despacha para o método visit específico"""
        
    def visit_BinaryOp(self, node: BinaryOp) -> Any: pass
    def visit_FunCall(self, node: FunCall) -> Any: pass
    # ... outros métodos visit
```

**Vantagens do Visitor**:
- Separação entre estrutura da AST e operações
- Facilita adição de novas operações sem modificar AST
- Permite múltiplas interpretações (interpretador, compilador, etc.)

## Bugs e Limitações

### Limitações Conhecidas

#### 1. **Tipos de Dados Limitados**
- **Suportados**: `int`, `bool` e `void`
- **Ausente**: `float`, `char`, `string`, arrays, structs
- **Impacto**: Restringe a expressividade da linguagem

#### 2. **Estruturas de Controle Básicas**
- **Ausente**: `for`, `do-while`, `switch/case`
- **Disponível apenas**: `if/else`, `while`

#### 3. **Conversões Implícitas**
- **Limitação**: Não há conversões automáticas entre tipos
- **Exemplo**: `bool resultado = 5;` gera erro (em C seria `true`)
- **Design**: Escolha intencional para maior segurança de tipos

#### 4. **Gerenciamento de Memória**
- **Limitação**: Sem alocação dinâmica
- **Ausente**: `malloc`, `free`, ponteiros

### Bugs Reportados

#### 1. **Precedência de Operadores** ⚠️
- **Severidade**: Média
- **Descrição**: Em algumas expressões complexas, a precedência pode não ser respeitada conforme C padrão
- **Workaround**: Use parênteses para garantir ordem de avaliação

#### 2. **Tratamento de Erros de Runtime** ⚠️
- **Severidade**: Baixa
- **Descrição**: Divisão por zero resulta em exception Python ao invés de erro semântico
- **Exemplo problemático**:
  ```c
  int x = 10 / 0;  // ZeroDivisionError não tratado
  ```

### Melhorias Futuras

#### Próximas Versões
1. **Mais tipos de dados** (`float`, `char`, `string`)
2. **Estruturas de controle adicionais** (`for`, `switch`)
3. **Conversões implícitas opcionais**
4. **Arrays e estruturas**
5. **Melhor tratamento de erros de runtime**

#### Possíveis Extensões
1. **Compilação para bytecode**
2. **Otimizações de código**
3. **Debugging interativo**
4. **Suporte a bibliotecas externas**

---

*Para reportar bugs ou sugerir melhorias, utilize o sistema de issues do repositório.*

## Recursos Implementados

### Tipos de Dados
- `int` - Números inteiros
- `bool` - Valores booleanos (`true`/`false`)
- `void` - Tipo vazio para funções

### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`
- **Relacionais**: `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Lógicos**: `&&`, `||`, `!`

### Estruturas de Controle
- **Condicionais**: `if`/`else`
- **Loops**: `while`
- **Funções**: Declaração, chamada e `return`

### Declarações
- Variáveis globais e locais
- Inicialização de variáveis
- Funções com parâmetros
- Blocos de código `{ }`

### Funções Built-in
- `print(expressao)` - Imprime valores e expressões

### Características das Variáveis
- **Declaração simples**: `int x;` (valor padrão: 0)
- **Com inicialização**: `int x = 42;`
- **Globais**: Declaradas fora de funções
- **Locais**: Declaradas dentro de funções ou blocos
- **Expressões como inicializadores**: `int resultado = a + b * 2;`

### Extensões
- Comentários multilinha com `/* texto */`  
- Comentários de linha única com `// texto`
- Inicialização de variáveis com valores
- Função `print()` para output

> **Nota**: O MicroC suporta ambos os tipos de comentários: multilinha (`/* */`) e linha única (`//`).

## Equipe

<table align="center" cellspacing="20" cellpadding="0">
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/170828870?v=4" width="100" style="border-radius: 50%;"><br>
      <strong><a href="https://github.com/caio-venancio">Caio Venâncio</a></strong><br>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/164296530?v=4" width="100" style="border-radius: 50%;"><br>
      <strong><a href="https://github.com/EnzoEmir">Enzo Emir</a></strong><br>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/125222370?v=4" width="100" style="border-radius: 50%;"><br>
      <strong><a href="https://github.com/MM4k">Marcelo Makoto</a></strong><br>
    </td>
  </tr>
</table>