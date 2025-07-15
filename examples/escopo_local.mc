/* Quando você declara uma variável dentro de uma função, essa variável é chamada local
Só existem enquanto a função estiver rodando
Não são visíveis fora da função.
Sempre que declara um bloco é uma novo escopo*/

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