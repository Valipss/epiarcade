/*
** EPITECH PROJECT, 2017
** my.h
** File description:
** includes
*/

#ifndef MY_H_
#define MY_H_

#include <stdarg.h>
#include <stdbool.h>

int my_putchar(char c);
int my_putstr(char const *str);
int my_put_nbr(int nb);
int my_strlen(char const *str);
char *my_revstr(char *str);
int my_put_uns_nbr(unsigned int n);
int my_put_nbr_base(int nb, char *base);
char *my_nbr_base(int nb, char *base);
int my_put_nbr_pointer(unsigned long long int nb, char *base);
int my_put_nbrspe(int nb);
int my_put_pointer(unsigned long long int nb);
int my_putspestr(char const *str);
int my_printf(char *msg, ...);
int disp_str(va_list ap);
int disp_int(va_list ap);
int disp_char(va_list ap);
int disp_unsint(va_list ap);
int disp_mod(va_list ap);
int disp_binary(va_list ap);
int disp_hexa(va_list ap);
int disp_octal(va_list ap);
int disp_spestr(va_list ap);
int disp_hexa_caps(va_list ap);
int disp_pointer(va_list ap);
int my_nbrlen(int nbr);
int my_atoi(char *str);
char *my_strcat(char *dest, char *src);
bool my_strcmp(char *str, char *cmp);
bool my_strncmp(char *str, char *cmp, int n);
char *my_strdup(char *str);
char **my_str_to_word_array(char *str, char separator);
char *get_next_line(int fd);
bool my_str_isnum(char *str);
char **my_revarray(char **array);
int my_arraylen(char **array);

#endif
