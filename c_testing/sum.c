#include <stdio.h>

int sum(int n) {
    int result = 0;
    for (int i = 1; i <= n; i++) {
        result += i;
    }
    return result;
}

int main() {
    int n = 10;
    printf("Sum of first %d numbers is %d\n", n, sum(n));
    return 0;
}