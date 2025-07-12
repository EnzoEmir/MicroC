## Interpretador de MicroC

Este repositório é dedicado ao trabalho final da disciplina de compiladores, no primeiro semestre de 2025.

##  Sobre o Projeto

O **MicroC** é um interpretador para uma versão simplificada da linguagem C, desenvolvido como projeto acadêmico. O projeto implementa as principais etapas de um compilador:

| Etapa | Status | Descrição |
|-------|--------|-----------|
| **Análise Léxica** | ✅ | Tokenização usando Lark |
| **Análise Sintática** | ✅ | Construção da AST |
| **Análise Semântica** | 🚧 | Verificação de tipos *(em desenvolvimento)* |
| **Interpretação** | ✅ | Execução via visitor pattern |

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
- Funções com parâmetros
- Blocos de código `{ }`

##  Como Usar

### Pré-requisitos
1. Certifique-se de estar no diretório raiz do projeto (onde está a pasta `MicroC/`)
2. Instale o `uv`:
   ```bash
   pip install uv
   ```

### Execução Básica
```bash
uv run MicroC arquivo.mc
```

Isso irá executar o arquivo MicroC especificado.

### Opções de Debug
| Comando | Descrição |
|---------|-----------|
| `uv run MicroC programa.c` | Execução normal |
| `uv run MicroC -l programa.c` | Mostra tokens do lexer |
| `uv run MicroC -c programa.c` | Mostra árvore sintática concreta (CST) |
| `uv run MicroC -t programa.c` | Mostra árvore sintática abstrata (AST) |
| `uv run MicroC -p programa.c` | Habilita debugger em caso de erro |

> **Nota**: O interpretador aceita arquivos com qualquer extensão. A extensão `.mc` é apenas uma convenção sugerida.

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
