#include <stdio.h>

int main(void) {
  int x, y;
  scanf("%d%*c %d%*c", &x, &y);
  printf("%d", x + y);
  return 0;
}