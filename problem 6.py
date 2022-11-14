# language: Python 3.10
# framework: IDLE

# references:
# Wikipedia
# Stackoverflow
# Python 3.10 documentation
# PROBLEM 6

# part 7

from random import randint
import functions as func

# BANK STORAGE

accounts = dict()  # accounts of all users and amount of money each one has
accounts['06749'] = []  # customer's account
accounts['35794'] = []  # another customer's account
accounts['20731'] = []  # merchant's account
info_storage = dict()   # a dictionary with information of all bills spent

# bank's public-private key
# everyone(i.e. a merchant and a customer) knows e and n

e = 65537
p = 103141
q = 197261
D = int(func.find_d(p, q, e))
n = p * q

# CUSTOMER(Alice)

k = 10  # nuber of chunks which are actually used
k_prime = 10  # number of chunks bank will choose to check
print('Hello! Because you do not have cash, suggest creating it. Do you want to create cash?(if yes - type yes, '
      'if no - type no)')
create_cash = str(input())

if create_cash == 'yes':
    print('How many bills do you want to create?')
    bills = int(input())

    for m in range(bills):
        print('What is the bill number?')
        bill = str(input())
        for key in info_storage:
            if bill == key:
                print('please choose a different bill number')
                bill = str(input())

        information = []  # a list with additional information that needs to be sent to the bank
        blinds = []  # a list with blinded f(x, y) for each chunk
        for_0 = []  # a list with information to reveal for each chunk if the merchant chooses 0
        for_1 = []  # a list with information to reveal for each chunk if the merchant chooses 1

        with open('to_sign' + bill + '.txt', 'w'):  # function used to clear the file from previous data
            pass

        to_sign = open('to_sign' + bill + '.txt', 'w')

        chunks = k + k_prime  # number of chunks for each bill

        I = '06749' + bill  # we have only one customer, so the account number for them is set

        for i in range(chunks):
            a = func.generating_numbers_strings()
            c = func.generating_numbers_strings()
            d = func.generating_numbers_strings()

            f, XOR, x, y = func.generating_f(a, c, d, I)

            blinded_message, factor = func.blind_message(n, e, int(f))

            for_0.append([XOR, d, x, str(factor)])
            for_1.append([a, c, y, str(factor)])
            information.append([str(factor), a, c, d])
            blinds.append(blinded_message)

            to_sign.write(str(blinded_message) + '\n')

        to_sign.close()

        print('Send the bill to the bank to verify it?(type yes/no)')
        for_bank = str(input())
        if for_bank == 'yes':

            # BANK CHECK

            to_sign = open('to_sign' + bill + '.txt', 'r')
            blinds = to_sign.readlines()  # bank reads blinded chunks from Alice

            checking = []  # a list with randomly selected chunks to check, bank will send it to alice

            for i in range(k_prime):  # bank randomly chooses chunks to open
                random = randint(0, len(blinds) - 1)  # randomly generated index
                line = blinds[random].replace('\n', '')
                # if bank chooses one chunk twice it'll need to choose again until it chooses the one that wasn't chosen
                while line in checking:
                    randomIndex = randint(0, len(blinds) - 1)
                    line = blinds[randomIndex].replace('\n', '')
                checking.append(line)

            to_sign.close()

            # end bank
            # start ALICE
            print('Send the information about chunks that the bank chose to the bank?(yes/no)')
            send_info = str(input())
            if send_info == 'yes':

                with open('bank_verify' + bill + '.txt', 'w'):
                    pass
                bank_verify = open('bank_verify' + bill + '.txt', 'w')

                # Alice writes the information for chosen chunks in correct (bank's) order
                for check in list(map(int, checking)):
                    check = str(check) + '\n'
                    index = blinds.index(check)
                    for j in range(len(information[index])):
                        bank_verify.write(information[index][j] + ' ')
                    bank_verify.write('\n')

                # Alice deletes information about "opened chunks", because she wouldn't need it later
                for i in range(len(checking)):
                    if checking[i] + '\n' in blinds:
                        index = blinds.index(checking[i] + '\n')
                        blinds.pop(index)
                        for_0.pop(index)
                        for_1.pop(index)

                bank_verify.close()

                # End ALICE
                # start bank

                bank_verify = open('bank_verify' + bill + '.txt', 'r')
                lines_bank = bank_verify.readlines()
                verify_info = []  # a list with information about chosen chunks from Alice
                for i in range(len(lines_bank)):
                    line = lines_bank[i]
                    info = line.split()
                    verify_info.append(info)

                with open('signed' + bill + '.txt', 'w'):
                    pass
                signed = open('signed' + bill + '.txt', 'w')
                flag = True  # Alice is not a cheater

                for i in range(len(verify_info)):

                    needed = verify_info[i]  # information about one chunk
                    r = func.fast_power(int(needed[0]), e, n)  # calculating r
                    r_inverse = func.modulo_multiplicative_inverse(r, n)
                    # finding an inverse to "divide" mods(because blinded chunks are mod n)
                    f_original = (int(checking[i]) * r_inverse) % n  # "dividing"

                    f_generated, XOR, x, y = func.generating_f(needed[1], needed[2], needed[3], I)
                    # generating f out of information alice provided using the same function as Alice

                    if f_original != int(f_generated):  # if they don't match - Alice is cheating
                        print('CHEATER DETECTED, account', I[:5], 'provided incorrect information')
                        flag = False
                        break

                if flag:
                    for j in range(len(blinds)):  # bank signs other k chunks

                        blinds[j] = blinds[j].replace('\n', '')

                        # creating signature on a blind message
                        signature_blind = func.signature_creation(int(blinds[j]), D, n)

                        signed.write(str(signature_blind) + '\n')
                        accounts['06749'] = [bill]  # bank deposits the cash to Alice's account

                signed.close()
                print('Do you want to spend this bill?(yes/no)')
                spend = str(input())
                if spend == 'yes':

                    # MERCHANT

                    with open('signed' + bill + '.txt', 'r') as signed_chunks:
                        chunks_merch = [line.rstrip() for line in signed_chunks]

                    with open('strings' + bill + '.txt', 'w'):
                        pass

                    strings = open('strings' + bill + '.txt', 'w')
                    # merchant randomly generates 0 or 1 for each chunk and sends them to Alice
                    for i in range(len(chunks_merch)):
                        string = randint(0, 1)
                        strings.write(str(string) + '\n')
                    strings.close()

                    # ALICE respond
                    print('Merchant asks for information about chunks, send them the information?(yes/no)')
                    spend_info = str(input())
                    if spend_info == 'yes':

                        # Alice reads the strings from the merchant
                        with open('strings' + bill + '.txt', 'r') as strings_read:
                            choice = [line.rstrip() for line in strings_read]

                        with open('merch_verify' + bill + '.txt', 'w'):
                            pass
                        merch_verify = open('merch_verify' + bill + '.txt', 'w')

                        for i in range(len(choice)):
                            # Alice writes the info for each chunk, depending on which string the merchant chose
                            if choice[i] == '0':

                                merch_verify.write(choice[i] + ' ')
                                for j in range(len(for_0[i])):
                                    if len(for_0[i]) - 1 == j:
                                        merch_verify.write(for_0[i][3] + ' ' + '\n')
                                    else:
                                        merch_verify.write(for_0[i][j] + ' ')

                            elif choice[i] == '1':

                                merch_verify.write(choice[i] + ' ')

                                for j in range(len(for_1[i])):

                                    if len(for_1[i]) - 1 == j:

                                        merch_verify.write(for_1[i][3] + ' ' + '\n')

                                    else:

                                        merch_verify.write(for_1[i][j] + ' ')

                        merch_verify.close()
                        # merchant check

                        # Merchant reads the information from Alice
                        with open('merch_verify' + bill + '.txt', 'r') as strings_read:
                            merch_verify = [line.rstrip() for line in strings_read]

                        with open('deposit' + bill + '.txt', 'w'):
                            pass
                        deposit = open('deposit' + bill + '.txt', 'w')

                        for i in range(len(merch_verify)):
                            verify = merch_verify[i].split()

                            f_customer = func.merchant_check(verify, chunks_merch[i], n, e)

                            # using different given data to get f of each chunk
                            if verify[0] == '0':  # given XOR, d, x

                                y_merch = func.generating_g(verify[1], verify[2])
                                f_merchant = func.generating_final_f(verify[3], y_merch)

                                if f_merchant == f_customer:
                                    # if both generated f's match merchant writes the information from Alice
                                    # and a blind signature in a file, which will be sent to bank
                                    for j in range(len(verify)):
                                        deposit.write(verify[j] + ' ')
                                    deposit.write(chunks_merch[i] + ' ' + '\n')
                                else:  # if not - the error message is displayed
                                    print('CHEATER DETECTED, customer provided incorrect signature and/or '
                                          'incorrect information about chunks')
                                    break

                            elif verify[0] == '1':  # given a, c, y

                                x_merch = func.generating_g(verify[1], verify[2])
                                f_merchant = func.generating_final_f(x_merch, verify[3])

                                if f_merchant == f_customer:
                                    # if both generated f's match merchant writes the information from Alice
                                    # and a blind signature in a file, which will be sent to bank
                                    for j in range(len(verify)):
                                        deposit.write(verify[j] + ' ')
                                    deposit.write(chunks_merch[i] + ' ' + '\n')
                                else:  # if not - the error message is displayed
                                    print('CHEATER DETECTED, customer provided incorrect signature and/or '
                                          'incorrect information about chunks')
                                    break

                        deposit.close()
                        # end merchant

                        # bank storage

                        with open('deposit' + bill + '.txt', 'r') as merch:
                            deposit_merch = [line.rstrip() for line in merch]
                        if deposit_merch == []:
                            print('Merchant did not provide any information about the bill')
                        else:
                            for i in range(len(deposit_merch)):  # bank repeats the verification and deposits the cash

                                verify_bank = deposit_merch[i].split()
                                f_customer_bank = func.merchant_check(verify_bank, verify_bank[5], n, e)

                                if verify_bank[0] == '0':

                                    y_merch = func.generating_g(verify_bank[1], verify_bank[2])
                                    f_merchant = func.generating_final_f(verify_bank[3], y_merch)

                                    if f_merchant == f_customer_bank:
                                        for key in info_storage:
                                            if info_storage[key][5] == verify_bank[5] and info_storage[key][0] != \
                                                    verify_bank[0]:
                                                I_restored = func.XOR(verify_bank[1], info_storage[key][1])
                                                print('CHEATER DETECTED. account ', I_restored[:5],
                                                      'spent the same bill', I_restored[5:], 'twice')
                                                break
                                    else:
                                        print('CHEATER DETECTED, customer provided incorrect signature and/or '
                                              'incorrect information about chunks')
                                        break

                                elif verify_bank[0] == '1':

                                    x_merch = func.generating_g(verify_bank[1], verify_bank[2])
                                    f_merchant = func.generating_final_f(x_merch, verify_bank[3])

                                    if f_merchant == f_customer_bank:
                                        for key in info_storage:  # checks if this bill was used before
                                            # if the blind signatures are the same with any bill
                                            # that was already used and the strings
                                            # generated by the mer chants are different bank gets the cheaters account
                                            if info_storage[key][5] == verify_bank[5] and info_storage[key][0] != \
                                                    verify_bank[0]:
                                                I_restored = func.XOR(verify_bank[1], info_storage[key][1])
                                                print('CHEATER DETECTED. account ', I_restored[:5],
                                                      'spent the same bill', I_restored[5:], 'twice')
                                                break
                                    else:
                                        print('CHEATER DETECTED, customer provided incorrect signature and/or '
                                              'incorrect information about chunks')
                                        break
                            # bank saves information about this bill in case Alice would use it again
                            info_storage[bill] = verify_bank
                            print(accounts['20731'])
                            for key in accounts:
                                if accounts[key] == [bill]:
                                    index = accounts[key].index(bill)
                                    accounts[key].pop(index)
                            accounts['20731'].append(bill)

                            print(accounts)
                            print(info_storage)
                    else:
                        print('Maybe next time! Thank yu for the interest shown!')
                else:
                    print('Thank you for creating and verifying this bill!')
            else:
                print('Thank you for the interest shown!')
        else:
            print('Thank you for creating this bill!')
else:
    print('Thank you for your interest! Goodbye!')
