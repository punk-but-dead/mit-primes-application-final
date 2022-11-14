# language: Python 3.10
# framework: IDLE

# references:

# Wikipedia
# Stackoverflow
# Python 3.10 documentation

# here are all the functions used in all programs

import hashlib
from random import randint


def gcd(number1, number2):

    # performs a Euclidean algorithm by dividing smaller number by bigger one
    # until one of the numbers is equal to zero
    # the number which isn't equal to zero is the gcd of these numbers

    while number1 != 0 and number2 != 0:
        if number1 > number2:
            number1 = number1 % number2
        else:
            number2 = number2 % number1
    return number1 + number2


def modulo_multiplicative_inverse(A, M):

    # assumes that M and A are co-primes
    # returns multiplicative modulo inverse of A under M

    return pow(A, -1, M)  # python function that returns a^(-1) mod M


def fast_power(base, power, MOD):

    # returns the result of a^b i.e. a**b mod m
    # works like this: 2^10 = 4^5 = 16^2 * 4 = 1024
    # because, for example: 24 mod 27 = 6 mod 27 * 4 mod 27
    # we can multiply reminders, not original numbers, which would be faster
    # we assume that a >= 1 and b >= 0

    result = 1
    while power > 0:
        # if power is odd
        if power % 2 == 1:
            result = (result * base) % MOD

        # divide the power by 2
        power = power // 2
        # multiply base to itself
        base = (base * base) % MOD

    return result


def find_d(P, Q, E):
    # calculates phi(n)
    phi = (P - 1) * (Q - 1)

    if gcd(E, phi) == 1:  # checks if e and phi are co-primes
        d = modulo_multiplicative_inverse(E, phi)  # calculates d
        return d  # returns d
    else:
        return 'incorrect encryption constant was used'  # if e and phi aren't co-primes, error message is displayed


def key_generation(P, Q, E, file):
    N = P * Q
    D = find_d(P, Q, E)  # finds d
    if isinstance(D, str):  # if D is not a number - the error message is displayed
        print(D)  # prints the error message
    else:
        file.write('public key: ')  # writes the key in the file
        file.write(str(N) + ', ')
        file.write(str(E) + ', ')
        file.write('private key: ')
        file.write(str(P) + ', ')
        file.write(str(Q) + ', ')
        file.write(str(D) + '\n')
        return N, E, P, Q, D  # returns the key (public, then private)


def encryption(M, N, E):
    # gives the message the power of E mod N(E and N - public key) = encrypts the message
    encrypted = fast_power(M, E, N)
    print('public key:', N, E)
    return encrypted  # returns the encrypted message


def decryption(P, Q, D, C):  # if we know d
    # returns C^D mod N, because C^D mod N = C^(E*D) mod N = C^1 mod N = C
    # (because it should be less than N)
    N = P * Q
    return fast_power(C, D, N)


def signature_check(M, S, N, E):
    verificated = fast_power(S, E, N)
    if verificated == M:
        return 'verification succeed'
    else:
        return 'verification failed'


def signature_creation(M, D, N):
    signature = fast_power(M, D, N)
    return signature


def blind_signature(M, P, Q, E):
    D = find_d(P, Q, E)  # finding d
    N = P * Q

    k = randint(1, N)  # generating random number

    r = fast_power(k, E, N)  # generating blinding factor
    blinded = (M % N) * r  # blinding message

    signature_blind = signature_creation(blinded, D, N)
    # returns (m*r^e)^d mod n = (m^d)*r mod n

    k_inverse = modulo_multiplicative_inverse(k, N)
    # finding an inverse for r to 'divide' signature_blind by r mod n(multiply by r^(-1) mod n),
    # to find the correct signature

    return (signature_blind * k_inverse) % N  # returns the original signature


def generating_numbers_strings():
    # generates random number
    # makes the number 10 decimal digits long
    # returns the number as a string

    number = randint(0, 2 ** 32 - 1)
    number_string = str(number)
    if len(number_string) < 10:
        len_zeros = 10 - len(number_string)
        number_string = len_zeros * '0' + number_string
        return number_string
    else:
        return number_string


def convert_base(num, to_base, from_base):
    # first convert to decimal number
    if isinstance(num, str):  # check if num is str
        n = int(num, from_base)  # converts to a decimal number, know its original base
    else:
        n = int(num)  # converts to a decimal number, assuming from_base < 10
    # now convert decimal to 'to_base' base
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = ""
    while n > 0:
        n, m = divmod(n, to_base)  # returns quotent and reminder in a tuple
        result += alphabet[m]  # m = reminder
    return result[::-1]  # reversing result to get final number


def XOR(a, I):
    # gets as an input two decimal numbers as strings
    # converts both to binary numbers
    # makes sure that each number is 10 binary digits long(if not program pads the number with zeros in the beginning)
    # then program uses XOR logic(compares two numbers by digits
    # and depending on its combination appends 1 or 0 to the resulting string) and creates a result
    # converts the result to decimal and pads it with zeros in the beginning if the number is less than 10 digits long
    # returns the result as a string

    binary_a = convert_base(a, 2, 10)
    binary_I = convert_base(I, 2, 10)
    if binary_a != binary_I:
        difference = len(binary_a) - len(binary_I)
        if difference > 0:
            binary_I = difference * '0' + binary_I
        else:
            binary_a = difference * '0' + binary_a
    XOR = ''
    for j in range(len(binary_a)):
        if binary_a[j] == '1' and binary_I[j] == '0':
            XOR += '1'
        elif binary_a[j] == '0' and binary_I[j] == '1':
            XOR += '1'
        else:
            XOR += '0'

    XOR_decimal = convert_base(XOR, 10, 2)
    if len(XOR_decimal) < 10:
        XOR_decimal = (10 - len(XOR_decimal)) * '0' + XOR_decimal
    return XOR_decimal


def generating_g(string1, string2):
    # using python basic function and the hashlib library
    # using md5 algorithm and encoding strings of decimal numbers(takes them as an input)
    # than we need to convert the output of the hash function to hex-number
    # and get the last 8 digits as the output of the functions
    # returns the string of 8 hex digits

    g_hash_function = hashlib.md5((string1 + string2).encode())
    g_hash_function = g_hash_function.hexdigest()
    output = g_hash_function[-8:]
    return output


def generating_final_f(x, y):
    # using python basic function and the hashlib library
    # using md5 algorithm and encoding strings of decimal numbers(takes them as an input)
    # then we need to convert the output of the hash function to hex-number
    # then get the first 8 digits as the output of the functions
    # at the end we need to convert 8 hex digits to decimal
    # returns a decimal number as a string

    f_hash_function = hashlib.md5((x + y).encode())
    f_hash_function = f_hash_function.hexdigest()
    f = f_hash_function[:8]
    f_decimal = convert_base(f, 10, 16)
    return f_decimal


def generating_f(a, c, d, I):
    # function takes 4 decimal numbers presented as strings as an input(a, c, d I)
    # generates XOR of a and I, then generates two g(i, j) hash functions
    # generates f(x, y) hash function
    # returns 4 decimal numbers as strings (f_decimal, XOR_decimal, x, y)

    XOR_decimal = XOR(a, I)
    x = generating_g(a, c)
    y = generating_g(XOR_decimal, d)
    f_decimal = generating_final_f(x, y)

    return f_decimal, XOR_decimal, x, y


def blind_message(N, E, M):
    k = randint(1, N)  # generating random number for the blinding factor

    r = fast_power(k, E, N)  # generating blinding factor
    blinded = (M * r) % N  # blinding message

    return blinded, k  # returns the blinded message and its blinding factor


def merchant_check(verify, blind_message, n, e):

    factor_inverse = modulo_multiplicative_inverse(int(verify[4]), n)
    # calculate an inverse of a blinding factor(original  randomly generated number)
    # to get a signature out of blinded one
    signature = (factor_inverse * int(blind_message)) % n  # calculating the original signature
    f_customer = str(fast_power(signature, e, n))  # decrypting the signature
    return f_customer