/* The scope of a variable in C is the block or the region in the program where a variable is declared, defined, and used. Outside this region, we cannot access the
variable, and it is treated as an undeclared identifier.

Variáveis declaradas fora de qualquer função são externas, ou globais

definição: cria a variável e reserva espaço na memória
declaração: só diz que a variável existe em outro lugar.*/

int global = 5;


int main(){
    int y = 3;

    return global + y;
}