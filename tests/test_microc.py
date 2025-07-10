import pytest
from MicroC.eval import eval

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
