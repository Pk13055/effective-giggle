#include<stdio.h>
int main() {
	int a, b;
	scanf("%d %d", &a, &b);
	for(int i = 0; i < 1000000; i++)
		printf("%d %d", a, b);
	return 0;
}
