# language: Python 3.10
# framework: IDLE

# references:
# Wikipedia
# Stackoverflow
# Python 3.10 documentation

# here are the coding part of the problems 1, 2, 3, and 5

import functions
from random import randint

print("What problem's code do you want to run? (type: 1.6 for problem 1 part 6, "
      "1.9 for problem 1 part 9, 2 for problem "
      "two(coding part), 3 for problem 3, 5 for problem 5 part 4(the coding part))")
problem = str(input())

# PROBLEM 1

if problem == '1.6':
    # part 6

    # file(problem 1.6.txt) with all needed inputs(each number on a different line, in that order):
    # modulus(m), number to inverse(k)
    # test data(in the same order as should be in file):
    # 7, -3
    # 3, 2
    # 5, 7
    # 4, 2
    # 120, 7
    # 22391, 100
    # 4699463680, 10799

    with open('problem 1.6.txt', 'r') as lines:
        input_1_6 = [line.rstrip() for line in lines]
    input_1_6 = list(map(int, input_1_6))  # makes a list integers out of any list(if it is possible)
    output_1_6 = open('output 1.6.txt', 'w')

    if functions.gcd(input_1_6[0], input_1_6[1]) == 1 and input_1_6[1] < input_1_6[0]:
        # if m and k are co-primes and m > k
        output_1_6.write(str(functions.modulo_multiplicative_inverse(input_1_6[1], input_1_6[0])) + ' ')
        output_1_6.write('mod' + ' ')
        output_1_6.write(str(input_1_6[0]))
    elif input_1_6[1] > input_1_6[0]:
        output_1_6.write('the number to inverse is greater than the modulus, please choose a different number')
    elif input_1_6[1] <= 0:
        output_1_6.write('the number to inverse is not positive, please choose a different number')
    elif functions.gcd(input_1_6[0], input_1_6[1]) != 1:
        output_1_6.write("the inverse doesn't exist")

    # results for part 6:
    # 1. 103 mod 120
    # 2. 19928 mod 22391
    # 3. 2613230799 mod 4699463680

elif problem == '1.9':
    # part 9

    # file(problem 1.9.txt) with all needed inputs(each number on a different line, in that order):
    # base, power, modulus
    # test data(in the same order as should be in file):
    # 0, 3, 6
    # -6, 7, 10
    # 0.5, 5, 9
    # 234561, 567839, 990887
    # 2, 4, 90

    with open('problem 1.9.txt', 'r') as lines:
        input_1_9 = [line.rstrip() for line in lines]
    output_1_9 = open('output 1.9.txt', 'w')

    input_1_9 = list(map(float, input_1_9))  # makes a list floats out of any list(if it is possible)

    # checking if any number is not an integer
    check = []  # a list with True of False values for each number(if it is an integer)
    for i in range(len(input_1_9)):
        check.append((input_1_9[i]).is_integer())

    if False not in check and input_1_9[0] > 0.0 and input_1_9[1] > 0.0 and input_1_9[2] > 0.0:
        output_1_9.write(str(functions.fast_power(input_1_9[0], input_1_9[1], input_1_9[2])) + ' ')
        output_1_9.write('mod' + ' ')
        output_1_9.write(str(input_1_9[2]))
    elif input_1_9[0] <= 0.0 or input_1_9[1] <= 0.0 or input_1_9[2] <= 0.0:
        output_1_9.write('one or more of the numbers is negative or equal to zero, please use different numbers')
    elif False in check:
        output_1_9.write('one or more of the numbers is not an integer, please use different numbers')

elif problem == '2':
    # PROBLEM 2

    # part 5

    # file(problem 2.txt) with all needed inputs(each number on different line, in that order):
    # p, q, e, m(message to encrypt), c(message to decrypt)
    # test data(the same order as should be in file):
    # 8783, 9133, 5, 34367293, 62190030
    # 23, 19, 5, 33, 264
    # 13, 7, 5, 4, 16
    # 13, 7, 7, 4, 16
    # 23, 19, 7, 33, 264
    # 3, 7, 8, 3, 5

    with open('problem 2.txt', 'r') as lines:
        input_2 = [line.rstrip() for line in lines]
    output_2 = open('output 2.txt', 'w')
    input_2 = list(map(int, input_2))  # makes a list integers out of any list(if it is possible)

    # key generation

    # if encryption constant wasn't correct function returns nothing and prints an error message
    if functions.key_generation(input_2[0], input_2[1], input_2[2], output_2) is None:
        error = 1  # nothing happens
    else:
        n, e, p, q, d = functions.key_generation(input_2[0], input_2[1], input_2[2], output_2)

        # results for part 1:
        # 1. public key: 91 5 private key: 13 7 29 and public key: 91 7 private key: 13 7 31
        # 2. public key: 437 5 private key: 23 19 317 and public key: 437 7 private key: 23 19 283

        # encryption

        output_2.write('encrypted: ')
        output_2.write(str(functions.encryption(input_2[3], n, e)) + '\n')
        # result for part 3: 295, public key: 437, 5

        # decryption

        output_2.write('decrypted: ')
        output_2.write(str(functions.decryption(p, q, d, input_2[4])))
        # result for part 3: 42

elif problem == '3':
    # PROBLEM 3

    # part 1

    # file(problem 3.txt) with all needed inputs(each number on a different line, in that order):
    # message, signature, n, e
    # test data(the same order as should be in file):
    # 123, 49259120, 80215139, 5
    # 555, 59131983, 80215139, 5
    # 1234567, 58520412, 80215139, 5

    with open('problem 3.txt', 'r') as lines:
        input_3 = [line.rstrip() for line in lines]
    output_3 = open('output 3.txt', 'w')

    input_3 = list(map(int, input_3))  # makes a list integers out of any list(if it is possible)

    output_3.write(functions.signature_check(input_3[0], input_3[1], input_3[2], input_3[3]))

    # results:
    # 1. verification succeed
    # 2. verification failed
    # message used for the signature was wrong, but d was right,
    # because the signature^e mod n was significantly less than original,
    # which suggests that the mult. inverse of e mod phi was used as a power
    # 3. verification succeed

    # part 2

    # pick a random number less than n and give it power e
    # if we make k - signature, the checker will give it power of e
    # and this pair will pass the verification
    # but there's not much you can gain from it
    # because it's nearly impossible to create a significant difference between the message, and it's signature
    # it would not look right, so people would notice that something is wrong

    k = randint(1, input_3[2] - 1)
    print('fake message and signature:', functions.fast_power(k, input_3[3], input_3[2]), k % input_3[2])
    print('fake signature check:',
          functions.signature_check(functions.fast_power(k, input_3[3], input_3[2]), k % input_3[2], input_3[2],
                                    input_3[3]))

elif problem == '5':
    # PROBLEM 5

    # part 4

    # file(problem 5.txt) with all needed inputs(each number on a different line, in that order):
    # message, p, q, e [data to calculate d and n]
    # test data(the same order as should be in file):
    # 123, 8783, 9133, 5
    # 300, 23, 19, 5
    # 30, 13, 7, 7
    # 45, 23, 17, 7
    # 12345678, 103141, 197261, 65537

    with open('problem 5.txt', 'r') as lines:
        input_5 = [line.rstrip() for line in lines]
    output_5 = open('output 5.txt', 'w')
    input_5 = list(map(int, input_5))  # makes a list integers out of any list(if it is possible)

    output_5.write('signature: ')
    output_5.write(str(functions.blind_signature(input_5[0], input_5[1], input_5[2], input_5[3])))
