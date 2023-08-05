from rpy2.robjects import r
# variable that can be changed as top of the calculus from 1 to numero
numero = input("Introduzca un numero entero mayor que uno: ")
# Assign the variable to the x parameter in the function in R code
r.assign('x', numero)
# Function in R that make the calculus
primos = r('''
        is.prime <- function(x)
        vapply(x, function(y) sum(y / 1:y == y %/% 1:y), integer(1L)) == 2L
        (1:x)[is.prime(1:x)]
        ''')
# Print the prime numbers
print(primos)