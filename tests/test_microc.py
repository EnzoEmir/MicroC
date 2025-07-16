import pytest
from MicroC.eval import eval
from MicroC.erros import *

# Teste simples: soma
microc_sum = '''
int main() {
    return 2 + 3;
}
'''

def test_sum():
    assert eval(microc_sum) == 5

# Teste: variável e atribuição
microc_var = '''
int main() {
    int x;
    x = 10;
    return x;
}
'''

def test_var_assignment():
    assert eval(microc_var) == 10

# Teste: if/else
microc_if = '''
int main() {
    if (1 == 1) {
        return 42;
    } else {
        return 0;
    }
}
'''

def test_if_else():
    assert eval(microc_if) == 42

# Teste: while
microc_while = '''
int main() {
    int i;
    i = 0;
    while (i < 3) {
        i = i + 1;
    }
    return i;
}
'''

def test_while():
    assert eval(microc_while) == 3

# Teste: função com parâmetro
microc_fun = '''
int soma(int a, int b) {
    return a + b;
}
int main() {
    return soma(4, 5);
}
'''

def test_function_call():
    assert eval(microc_fun) == 9

# Teste: função simples sem parâmetros (baseado em funcao.mc)
microc_simple_function = '''
int f() {
    return 42;
}

int main() {
    return f();
}
'''

def test_simple_function():
    assert eval(microc_simple_function) == 42

# Teste: variável global (baseado em example.mc)
microc_global_var = '''
int x;

int soma(int a, int b) {
    return a + b;
}

int main() {
    x = soma(2, 3);
    return x;
}
'''

def test_global_variable():
    assert eval(microc_global_var) == 5

# Teste: função com 3 parâmetros (baseado em example_soma3.mc)
microc_three_params = '''
int x;

int soma3(int a, int b, int c) {
    return a + b + c;
}

int main() {
    x = soma3(1, 2, 3);
    return x;
}
'''

def test_function_three_params():
    assert eval(microc_three_params) == 6

# Teste: escopo de função (baseado em escopo_funcao.mc)
microc_function_scope = '''
int f() {
    int x = 10;
    int y = 5;
    return x + y;
}

int main() {
    return f();
}
'''

def test_function_scope():
    assert eval(microc_function_scope) == 15

# Teste: escopo global com inicialização (baseado em escopo_global.mc)
microc_global_scope = '''
int global = 5;

int main(){
    int y = 3;
    return global + y;
}
'''

def test_global_scope():
    assert eval(microc_global_scope) == 8

# Teste: escopo em if (baseado em escopo_if.mc)
microc_if_scope = '''
int main(){
    int x = 10;
    if (x > 5) {
        int y = 20;
        x = x - y;
    }
   return x;
}
'''

def test_if_scope():
    assert eval(microc_if_scope) == -10

# Teste: escopo local com blocos aninhados (baseado em escopo_local.mc)
microc_local_scope = '''
int main()
{
    {
        int x;
        x = 10;
        int y;
        y = 20;
        {
            {
                int y;
                y = 40;
                x = x + 1;
                y = y + 1;
            }
        }
        return y;
    }
    return 0;
}
'''

def test_local_scope():
    assert eval(microc_local_scope) == 20

# Teste: escopo em while (baseado em escopo_while.mc)
microc_while_scope = '''
int main() {
    int x = 0;
    int y = 2;
    while (x < 1) {
        int y = 5;
        x = x + 1;
    }
    return x + y; 
}
'''

def test_while_scope():
    assert eval(microc_while_scope) == 3

# Teste: declaração de variável separada da inicialização (baseado em var_decl.mc)
microc_var_declaration = '''
int main(){
    int x;
    x = 10;
    return x;
}
'''

def test_variable_declaration():
    assert eval(microc_var_declaration) == 10

# Testes adicionais para operadores aritméticos
microc_arithmetic = '''
int main() {
    int a = 10;
    int b = 3;
    return a + b + a;
}
'''

def test_arithmetic_operations():
    assert eval(microc_arithmetic) == 23  # 10 + 3 + 10 = 23

# Teste para operadores relacionais
microc_relational = '''
int main() {
    int x = 5;
    int y = 3;
    if (x >= y) {
        return 1;
    }
    return 0;
}
'''

def test_relational_operators():
    assert eval(microc_relational) == 1

# Teste para operadores lógicos
microc_logical = '''
int main() {
    int a = 1;
    int b = 0;
    if (a == 1) {
        if (b == 0) {
            return 10;
        }
    }
    return 5;
}
'''

def test_logical_operators():
    assert eval(microc_logical) == 10

# Teste para while mais complexo
microc_complex_while = '''
int main() {
    int sum = 0;
    int i = 1;
    while (i <= 5) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}
'''

def test_complex_while():
    assert eval(microc_complex_while) == 15  # 1+2+3+4+5 = 15

# Teste para if-else aninhado
microc_nested_if = '''
int main() {
    int x = 10;
    if (x > 5) {
        if (x > 15) {
            return 1;
        } else {
            return 2;
        }
    } else {
        return 3;
    }
}
'''

def test_nested_if():
    assert eval(microc_nested_if) == 2

# Teste para operador de negação
microc_negation = '''
int main() {
    int x = 5;
    int y = 0 - x;
    return y;
}
'''

def test_negation():
    assert eval(microc_negation) == -5

# Teste para múltiplas variáveis globais
microc_multiple_globals = '''
int a = 10;
int b = 20;
int c;

int main() {
    c = a + b;
    return c;
}
'''

def test_multiple_globals():
    assert eval(microc_multiple_globals) == 30

# Teste para função que não retorna valor
microc_void_function = '''
int x;

int increment() {
    x = x + 1;
    return x;
}

int main() {
    x = 5;
    increment();
    return x;
}
'''

def test_void_function():
    assert eval(microc_void_function) == 6

# Teste para operações com parênteses
microc_parentheses = '''
int main() {
    int a = 2;
    int b = 3;
    int c = 4;
    return (a + b) * c;
}
'''

def test_parentheses():
    assert eval(microc_parentheses) == 20

# Teste para comparações múltiplas
microc_comparisons = '''
int main() {
    int x = 10;
    if (x > 5) {
        if (x < 15) {
            return 1;
        }
    }
    return 0;
}
'''

def test_comparisons():
    assert eval(microc_comparisons) == 1

# Teste para função recursiva simples (fatorial iterativo)
microc_factorial_iterative = '''
int factorial(int n) {
    int result = 1;
    int i = 1;
    while (i <= n) {
        result = result * i;
        i = i + 1;
    }
    return result;
}

int main() {
    return factorial(4);
}
'''

def test_factorial_iterative():
    assert eval(microc_factorial_iterative) == 24

# ===========================================
# TESTES PARA FUNCIONALIDADE PRINT
# ===========================================

# Teste básico de print
microc_print_basic = '''
int main() {
    print(42);
    return 0;
}
'''

def test_print_basic():
    import io
    import sys
    from contextlib import redirect_stdout
    
    # Captura a saída do print
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_basic)
    
    output = f.getvalue().strip()
    assert "42" in output
    assert result == 0

# Teste de print com variável
microc_print_variable = '''
int main() {
    int x = 10;
    print(x);
    return x;
}
'''

def test_print_variable():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_variable)
    
    output = f.getvalue().strip()
    assert "10" in output
    assert result == 10

# Teste de print com expressão
microc_print_expression = '''
int main() {
    int a = 5;
    int b = 3;
    print(a + b);
    return a * b;
}
'''

def test_print_expression():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_expression)
    
    output = f.getvalue().strip()
    assert "8" in output  # a + b = 5 + 3 = 8
    assert result == 15   # a * b = 5 * 3 = 15

# Teste de múltiplos prints
microc_print_multiple = '''
int main() {
    int x = 1;
    int y = 2;
    print(x);
    print(y);
    print(x + y);
    return 0;
}
'''

def test_print_multiple():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_multiple)
    
    output = f.getvalue().strip()
    lines = output.split('\n')
    
    # Verifica se há pelo menos 3 linhas de saída (sem contar o resultado final)
    assert len(lines) >= 3
    # Verifica se os valores estão presentes
    assert "1" in output
    assert "2" in output
    assert "3" in output
    assert result == 0

# Teste de print em loop
microc_print_loop = '''
int main() {
    int i = 0;
    while (i < 3) {
        print(i);
        i = i + 1;
    }
    return i;
}
'''

def test_print_loop():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_loop)
    
    output = f.getvalue().strip()
    assert "0" in output
    assert "1" in output
    assert "2" in output
    assert result == 3

# Teste de print em função
microc_print_function = '''
int print_and_return(int value) {
    print(value);
    return value * 2;
}

int main() {
    int result = print_and_return(5);
    return result;
}
'''

def test_print_function():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_function)
    
    output = f.getvalue().strip()
    assert "5" in output
    assert result == 10

# ===========================================
# TESTES ADICIONAIS PARA DECLARAÇÕES DE VARIÁVEIS
# ===========================================

# Teste de declaração de variável com inicialização
microc_var_init = '''
int main() {
    int x = 42;
    int y = x + 8;
    return y;
}
'''

def test_var_initialization():
    assert eval(microc_var_init) == 50

# Teste de variável global com inicialização e modificação local
microc_var_global_local = '''
int global_var = 100;

int main() {
    int local_var = 50;
    global_var = global_var + local_var;
    return global_var;
}
'''

def test_var_global_local():
    assert eval(microc_var_global_local) == 150

# Teste de múltiplas declarações em sequência
microc_var_multiple_decl = '''
int main() {
    int a = 1;
    int b = 2;
    int c = 3;
    int d = a + b + c;
    return d;
}
'''

def test_var_multiple_declarations():
    assert eval(microc_var_multiple_decl) == 6

# Teste de variável declarada e inicializada em bloco
microc_var_block_scope = '''
int main() {
    int result = 0;
    {
        int temp = 10;
        result = temp * 2;
    }
    return result;
}
'''

def test_var_block_scope():
    assert eval(microc_var_block_scope) == 20

# Teste de variável com operações complexas
microc_var_complex = '''
int calculate(int base) {
    int doubled = base * 2;
    int added = doubled + 10;
    return added;
}

int main() {
    int input = 5;
    int result = calculate(input);
    return result;
}
'''

def test_var_complex_operations():
    assert eval(microc_var_complex) == 20  # (5 * 2) + 10 = 20

# Teste combinando print e declarações de variáveis
microc_print_var_combined = '''
int main() {
    int x = 7;
    int y = 3;
    int sum = x + y;
    print(sum);
    int product = x * y;
    print(product);
    return sum + product;
}
'''

def test_print_var_combined():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        result = eval(microc_print_var_combined)
    
    output = f.getvalue().strip()
    assert "10" in output  # x + y = 7 + 3 = 10
    assert "21" in output  # x * y = 7 * 3 = 21
    assert result == 31    # sum + product = 10 + 21 = 31

# ===========================================
# TESTES PARA TRATAMENTO DE ERROS
# ===========================================

# Teste para função main não definida
def test_missing_main_function():
    microc_no_main = '''
    int soma(int a, int b) {
        return a + b;
    }
    '''
    
    with pytest.raises(UndefinedFunctionError) as exc_info:
        eval(microc_no_main)
    
    assert "main" in str(exc_info.value)

# Teste para variável não definida
def test_undefined_variable():
    microc_undefined_var = '''
    int main() {
        return x;
    }
    '''
    
    with pytest.raises(UndefinedVariableError) as exc_info:
        eval(microc_undefined_var)
    
    assert "x" in str(exc_info.value)

# Teste para função não definida
def test_undefined_function():
    microc_undefined_func = '''
    int main() {
        return foo();
    }
    '''
    
    with pytest.raises(UndefinedFunctionError) as exc_info:
        eval(microc_undefined_func)
    
    assert "foo" in str(exc_info.value)

# Teste para número incorreto de argumentos - poucos argumentos
def test_wrong_argument_count_few():
    microc_few_args = '''
    int soma(int a, int b) {
        return a + b;
    }
    
    int main() {
        return soma(5);
    }
    '''
    
    with pytest.raises(ArgumentCountError) as exc_info:
        eval(microc_few_args)
    
    error = exc_info.value
    assert error.func_name == "soma"
    assert error.expected == 2
    assert error.got == 1

# Teste para número incorreto de argumentos - muitos argumentos
def test_wrong_argument_count_many():
    microc_many_args = '''
    int soma(int a, int b) {
        return a + b;
    }
    
    int main() {
        return soma(1, 2, 3);
    }
    '''
    
    with pytest.raises(ArgumentCountError) as exc_info:
        eval(microc_many_args)
    
    error = exc_info.value
    assert error.func_name == "soma"
    assert error.expected == 2
    assert error.got == 3

# Teste para atribuição a variável não declarada
def test_assignment_to_undefined_variable():
    microc_undefined_assignment = '''
    int main() {
        x = 10;
        return x;
    }
    '''
    
    with pytest.raises(UndefinedVariableError) as exc_info:
        eval(microc_undefined_assignment)
    
    assert "x" in str(exc_info.value)

# Teste para uso de variável em escopo incorreto
def test_variable_scope_error():
    microc_scope_error = '''
    int main() {
        {
            int x = 10;
        }
        return x;
    }
    '''
    
    with pytest.raises(UndefinedVariableError) as exc_info:
        eval(microc_scope_error)
    
    assert "x" in str(exc_info.value)

# Teste para função sem argumentos chamada com argumentos
def test_no_params_with_args():
    microc_no_params_with_args = '''
    int getAnswer() {
        return 42;
    }
    
    int main() {
        return getAnswer(5);
    }
    '''
    
    with pytest.raises(ArgumentCountError) as exc_info:
        eval(microc_no_params_with_args)
    
    error = exc_info.value
    assert error.func_name == "getAnswer"
    assert error.expected == 0
    assert error.got == 1

# Teste para verificar que erros semânticos são detectados corretamente
def test_semantic_error_properties():
    microc_undefined = '''
    int main() {
        return undefined_var;
    }
    '''
    
    with pytest.raises(SemanticError) as exc_info:
        eval(microc_undefined)
    
    # Verifica se é uma SemanticError
    assert isinstance(exc_info.value, SemanticError)
    # Verifica se é especificamente UndefinedVariableError
    assert isinstance(exc_info.value, UndefinedVariableError)

# Teste para múltiplos erros em sequência
def test_multiple_errors():
    # Primeiro erro: função não definida
    microc_error1 = '''
    int main() {
        return nonexistent();
    }
    '''
    
    with pytest.raises(UndefinedFunctionError):
        eval(microc_error1)
    
    # Segundo erro: variável não definida
    microc_error2 = '''
    int main() {
        return missing_var;
    }
    '''
    
    with pytest.raises(UndefinedVariableError):
        eval(microc_error2)

# Teste para verificar que o código válido ainda funciona
def test_valid_code_still_works():
    microc_valid = '''
    int multiply(int a, int b) {
        return a * b;
    }
    
    int main() {
        int x = 4;
        int y = 5;
        return multiply(x, y);
    }
    '''
    
    # Este não deve gerar erro
    result = eval(microc_valid)
    assert result == 20
