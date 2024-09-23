# Código basado en: https://youtu.be/D_PfV_IcUdA?si=RP0y8clh3PWWB_HT
# Este codigo es simplemente una version simple de RSA, posibles mejoras:
# is_prime(number) ha sido mejorada cambiando number // 2 por sqrt(number), la explicacion es un poco compleja
# en resumen si tenemos un numero compuesto (no primo) n, parte de sus factores seran menores a su raiz cuadrada mientras que 
# otros seran mayores puesto que si todos fueran mayores su producto seria superior a n y si todos fusen menores su
# producto seria menor que n. Por tanto si n es divisible por algun numero al menos uno de ellos debe ser menor o igual a sqrt(n)
# En cualquier caso, si no te has enterado de lo arriba, la funcion is_prime(number) creo que se podria mejorar aun mas implementando
# el test de primalidad de Miller-Rabin, no estoy segura porque este metodo realmente es estadistico por lo que NO encuentra
# numeros primos sino numeros probablemente primos.

# Como ya se menciona la busqueda de la inversa modular deberia de mejorarse con el Algoritmo Extendido de Euclides
# Al final de este fichero comentado se encuentra una implementacion dada por chatgpt, por ahora no he comprobado su funcionamiento
# por lo que no he sustituido el codigo inicial

# La generacion de numeros primos podria mejorarse con la criba de Eratostenes, probablemente haciendo bien esto nos podamos ahorrar
# utilizar el test de primalidad de Miller-Rabin no? Preguntar profesor

# Segun chatgpt, pendiente de investigar también
# Aunque estás asegurándote de que e sea coprimo con φ(n), en RSA generalmente se prefiere elegir ciertos valores estándar para e, 
# como 65537 (una constante que es común en muchas implementaciones de RSA), ya que es un número primo pequeño
# y hace que la exponenciación sea más rápida, sin comprometer la seguridad.

# e = 65537
# if math.gcd(e, phi_n) != 1:
#     raise ValueError("65537 no es coprimo con φ(n), elige otro p y q")

# p y q deberian de ser primos mucho mas grandes al menos 1024 bits para que n tenga 2048

# bueno pues vaya lio, resulta que esto es raw RSA pero que deberiamos de incluir un padding con OAEP o PKCS#1 v1.5 para aminorar
# las vulnerabilidades, ademas, normalmente no se encriptaria caracter a caracter sino que se crearian bloques previamente
import random
import math

def is_prime(number):
    # el numero 1 en teoria de numeros no se considera primo ya que no tiene como unicos divisores (2) al 1 
    # y a si mismo sino que solo de tiene (1) asi mismo (si un poco raro lo se)
    # realmente es considerado una unidad y no se clasifica ni como primo ni como compuesto
    if number < 2:
        return False
    # +1 porque la funcion range en python aunque incluye el valor inicial excluye el final

    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

# Si los pasos anteriores han ido bien el error no debería de salir
# Esto se puede mejorar aplicando el Algoritmo extendido de Euclides
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("No existe la inversa modular")

# No son grandes realmente
p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)

# Este paso es realmente importante, si p y q fuesen el mismo numero primo compremeteriamos gravemente
# la seguridad del sistema ya que en lugar de p*q estariamos ante p^2 lo cual es reversible mediante
# una raíz cuadrada si se llega a conocer n
# ej p = q = 3 -> 3^2 = 9 -> sqrt(9) = 3 = p = q 
#  p = 3 q = 7 -> 3*7 = 21 -> sqrt(21) = 5.19... no se puede retroceder
while p == q:
    q = generate_prime(1000, 5000)

n = p * q
phi_n = (p-1) * (q-1)

# ojo, no os confundais con range, en este caso phi_n-1 si que puede ser el numero aleatorio elegido
e = random.randint(3, phi_n-1)
# comprobamos si son coprimos, y mientras no lo sean generamos otra e
while math.gcd(e, phi_n) != 1:
    e = random.randint(3, phi_n-1)

d = mod_inverse(e, phi_n)

print("Public Key: ", e)
print("Private Key: ", d)
print("n: ", n)
print("Phi of n: ", phi_n)
print("p: ", p)
print("q: ", q)

message = "¡Hola! Esto es RSA"
# con ord pasamos los caracteres a su valor ASCII para tener numeros con los que operar facilmente
message_encoded = [ord(char) for char in message]
# (m ^ e) mod n = c
# la funcion pow(base, exponente, modulo) se puede usar con 3 argumentos 
ciphertext = [pow(char, e, n) for char in message_encoded]

# es una lista se podria unir en un string pero creo que no importa
print(ciphertext)

# (c ^ d) mod n = m
message_decoded = [pow(char, d, n) for char in ciphertext]
message = "".join(chr(char) for char in message_decoded)

print(message)


# def extended_gcd(a, b):
#     if a == 0:
#         return b, 0, 1
#     gcd, x1, y1 = extended_gcd(b % a, a)
#     x = y1 - (b // a) * x1
#     y = x1
#     return gcd, x, y

# def mod_inverse(e, phi):
#     gcd, x, _ = extended_gcd(e, phi)
#     if gcd != 1:
#         raise ValueError("No existe la inversa modular")
#     return x % phi