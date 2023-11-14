import generate_prime
import rsa
import os
from datetime import datetime


def rsa_key_gen():
    """
    Generates new keys
    :return: the private and public keys
    :rtype: tuple[tuple[int]]
    """

    # getting key size
    print("Enter desired key size:")
    key_size = input("2048/3072/4096: ")  # key size less than 2048 bit isn't secure enough
    while key_size not in ['2048', '3072', '4096']:
        print('Invalid option!')
        key_size = input("2048/3072/4096: ")

    # generating keys
    key_size = int(key_size)
    print('Generating...')
    p, q = generate_prime.get_prime(key_size // 2), generate_prime.get_prime(key_size // 2)
    public, private = rsa.get_keys(p, q)

    print('\nThe generated keys are:')
    print(f'\tRSA Public Key:\n\t\t- Modulus (n): {public[0]}\n\t\t- Public Exponent (e): {public[1]}\n')
    print(f'\tRSA Private Key:\n\t\t- Modulus (n): {private[0]}\n\t\t- Private Exponent (d): {private[1]}\n')

    print("Would you like to save the keys in a file?")
    choice_save = input("Y/N: ")
    while choice_save not in ['Y', 'N', 'y', 'n']:
        print('Invalid option!')
        choice_save = input("Y/N: ")

    # saving keys into file
    if choice_save.upper() == 'Y':
        path = input('Please Specify a file path to save keys:')
        while os.path.isdir(os.path.dirname(path)) is False:
            print("Invalid path!")
            path = input('Please Specify a file path to save keys:')

        with open(path, 'w') as f:
            now = datetime.now()
            f.write(f'RSA Keys: {now.strftime("%d/%m/%Y %H:%M:%S")}:')
            f.write(f"\n\tRSA Public Key:\n\t\t- Modulus (n): {public[0]}\n\t\t- Public Exponent (e): {public[1]}\n")
            f.write(
                f"\n\tRSA Private Key:\n\t\t- Modulus (n): {private[0]}\n\t\t- Private Exponent (d): {private[1]}\n")
            print("Keys have been saved successfully!")

    return public, private


def rsa_encryption(self_public_key):
    """
    encrypts a message using RSA with user's chosen keys
    :param self_public_key: The user's self private key, used optionally for self-encryption
    :type: int
    :return: the encrypted message's blocks
    :rtype: list[int]
    """

    msg = input("Please Enter the message to encrypt: ")

    # assuming not self-encrypting
    choice_key = '1'
    # checking if self-encrypting, in-case self-keys found
    if self_public_key is not None:
        print("Choose one of the following options:\n"
              "\t(1). Provide recipient's public key.\n"
              "\t(2). Use the last generated public key (self-encrypt).")
        choice_key = input("1/2: ")
        while choice_key not in ['1', '2']:
            print('Invalid option!')
            choice_key = input("1/2: ")

    # getting recipient's public key
    if choice_key == '1':
        print("\nGetting recipient's public key (n e): ")

        # getting modulus 'n'
        n_str = input('\t(1). Enter recipient\'s modulus (n): ')
        while n_str.isnumeric() is False or int(n_str).bit_length() < 1024:
            if n_str.isnumeric() is False:
                print("\t\tPlease enter an int!")
            else:
                print("Modules is too small. For better security, pick around a 2048-bit sized modulus or bigger.")

            n_str = input("\t(1). Enter recipient\'s modulus (n): ")
        n = int(n_str)

        # getting public exponent 'e'
        e_str = input('\t(2). Enter recipient\'s public exponent (e): ')
        while e_str.isnumeric() is False:
            print("\t\tPlease enter an int!")
            e_str = input("'\t(2). Enter recipient\'s public exponent (e): ")
        e = int(e_str)

    # using self-key
    else:
        n, e = self_public_key[0], self_public_key[1]

    # encrypting message
    enc_blocks = rsa.encrypt(msg, (n, e))
    print(f'\nThe encrypted message blocks are:')
    for i in enc_blocks:
        print(f'\t- {i}')

    print("\nWould you like to save the encrypted message in a file?")
    choice_save = input("Y/N: ")
    while choice_save not in ['Y', 'N', 'y', 'n']:
        print('Invalid option!')
        choice_save = input("Y/N: ")

    # saving to file
    if choice_save.upper() == 'Y':
        path = input('\nPlease Specify a file path to save the encrypted message:')
        while os.path.isdir(os.path.dirname(path)) is False:
            print("Invalid path!")
            path = input('Please Specify a file path to save the encrypted message:')

        with open(path, 'w') as f:
            now = datetime.now()
            f.write(f'RSA encrypted message blocks: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            for i in enc_blocks:
                f.write(f'\t- {i}\n')
            print("\nEncrypted message has been saved successfully!")


def rsa_decryption(self_private_key):
    """
    decrypts a message using RSA with user's chosen keys
    :param self_private_key: The user's self private key, used optionally for self-decryption
    :type: int
    :return: the decrypted message
    :rtype: str
    """

    # getting encrypted blocks
    print("Choose one of the next options for inputting encrypted blocks:\n"
          "\t(1). Input blocks one by one.\n"
          "\t(2). Input block from a file (this program file-format).")
    choice_dec = input('1/2: ')
    while choice_dec not in ['1', '2']:
        print('Invalid option!')
        print("Choose one of the next options for inputting encrypted blocks:\n"
              "\t(1). Input blocks one by one.\n"
              "\t(2). Input block from file (this program format).")
        choice_dec = input('1/2: ')
    print()

    dec_blocks = []

    # getting blocks one by one
    if choice_dec == '1':
        print("Enter the decrypted blocks, seperated by 'Enter' one by one. Enter '.' to stop:")
        cur_block = input('- ')
        while cur_block.isnumeric() is False and cur_block != '.':
            print("\t\tPlease enter an int!")
            cur_block = input('- ')

        while cur_block != '.':
            dec_blocks.append(int(cur_block))

            cur_block = input('- ')
            while cur_block.isnumeric() is False and cur_block != '.':
                print("\t\tPlease enter an int!")
                cur_block = input('- ')

    # getting blocks from a file generated by this program's encryption process
    else:
        # runs while the given file format is invalid
        while True:
            # getting and checking existence of the file
            path = input('Please specify the encrypted message\'s file path: ')
            while os.path.isdir(os.path.dirname(path)) is False:
                print("Invalid path!")
                path = input('Please specify the encrypted message\'s file path: ')

            with open(path, 'r') as f:
                # getting blocks
                lines = f.readlines()
                for line in lines[1:]:
                    try:
                        cur_block = int(line[3:-1])  # skipping the '\t- ' at the beginning, and the '\n' at the end.
                        dec_blocks.append(cur_block)
                    # invalid format
                    except ValueError:
                        print('File\'s format isn\'t correct. Please specify an other file.')
                        continue
            break

    # assuming not self-encrypting
    choice_key = '1'
    # checking if self-encrypting, in-case self-keys found
    if self_private_key is not None:
        print("Choose one of the following options:\n"
              "\t(1). Provide recipient's private key.\n"
              "\t(2). Use the last generated private key (self-decrypt).")
        choice_key = input("1/2: ")
        while choice_key not in ['1', '2']:
            print('Invalid option!')
            choice_key = input("1/2: ")

    if choice_key == '1':
        # getting recipient's private key
        print("Enter recipient's public key (n e): ")

        n_str = input('\t(1). Enter recipient\'s modulus (n): ')
        while n_str.isnumeric() is False:
            print("\t\tPlease enter an int!")
            n_str = input("'\t(1). Enter recipient\'s modulus (n): ")
        n = int(n_str)

        d_str = input('\t(2). Enter recipient\'s private exponent (d): ')
        while d_str.isnumeric() is False:
            print("\t\tPlease enter an int!")
            d_str = input("'\t(2). Enter recipient\'s public exponent (d): ")
        d = int(d_str)

    else:
        # using self-keys
        n, d = self_private_key[0], self_private_key[1]

    # decrypting  message
    dec_msg = rsa.decrypt(dec_blocks, (n, d))
    print(f'\nThe decrypted message is:\n\t{dec_msg}')

    # saving to file
    print("\nWould you like to save the decrypted message in a file?")
    choice_save = input("Y/N: ")
    while choice_save not in ['Y', 'N', 'y', 'n']:
        print('Invalid option!')
        choice_save = input("Y/N: ")

    if choice_save.upper() == 'Y':
        path = input('\nPlease Specify a file path to save the decrypted message:')
        while os.path.isdir(os.path.dirname(path)) is False:
            print("Invalid path!")
            path = input('Please Specify a file path to save the decrypted message:')

        with open(path, 'w') as f:
            now = datetime.now()
            f.write(f'RSA decrypted message: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            f.write(f'\t{dec_msg}')
            print("\nDecrypted message has been saved successfully!")


def main():
    print('================================================================\n'
          '\t\tRSA Implementation By Yahav Bragin\n'
          '================================================================')

    choice = public = private = None

    while choice != '0':
        print("\n\nChoose one of the next options:\n"
              "\t(0) End.\n"
              "\t(1) RSA Keys Generation.\n"
              "\t(2) RSA Encryption.\n"
              "\t(3) RSA Decryption.")

        choice = input('0/1/2/3: ')
        while choice not in ['0', '1', '2', '3']:
            print('Invalid option!')
            print("Choose one of the next options:\n"
                  "\t(0) End.\n"
                  "\t(1) RSA Keys Generation.\n"
                  "\t(2) RSA Encryption.\n"
                  "\t(3) RSA Decryption.")

            choice = input('0/1/2/3: ')

        print('\n')
        if choice == '1':
            public, private = rsa_key_gen()
        elif choice == '2':
            rsa_encryption(public)
        elif choice == '3':
            try:
                rsa_decryption(private)
            except Exception:
                print("Invalid\Incorrect private exponent for the given modulus")


if __name__ == '__main__':
    main()
