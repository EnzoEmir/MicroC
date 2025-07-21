int main() {
    int a = 5;
    int b = 2;
    int c = 9;

    // bubble sort manual entre 3 variáveis
    int temp;
    if (a > b) {
        temp = a; a = b; b = temp;
    }
    if (a > c) {
        temp = a; a = c; c = temp;
    }
    if (b > c) {
        temp = b; b = c; c = temp;
    }

    print(a); print(b); print(c); // ordenado
    return 0;
}