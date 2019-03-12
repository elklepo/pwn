# define HOST_c2l(c,l)  (l =(((unsigned long)(*((c)++)))<<24),          \
                         l|=(((unsigned long)(*((c)++)))<<16),          \
                         l|=(((unsigned long)(*((c)++)))<< 8),          \
                         l|=(((unsigned long)(*((c)++)))    )           )

int main()
{
int liczba;
char tablica[4] = {0xff, 0xaa, 0xcc, 0xee};
char *x = (char*)tablica;

HOST_c2l(x, liczba);
printf("%8x", liczba);
return 0;
}
