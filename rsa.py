import my_utilities
import os


def get_keys(p, q):
    """
    Generates RSA private and public keys using given numbers assumed to be primes
    :param p: first prim
    :type p: int
    :param q: second prime
    :type q: int
    :return: the private and public keys in a tuple ((n, e), (n, d))
    :rtype: tuple[tuple[int]]
    """

    n = p * q  # calculating modulus

    phi_n = (p - 1) * (q - 1)  # calculating phi_n, almost impossible for one who only knows n, and not p, q

    e = 65537  # public exponent, common in industry

    # calculating the multiplicative inverse of e: d - the private exponent
    d = my_utilities.mod_inverse(e, phi_n)

    return (n, e), (n, d)


def pkcs1_v1_5_pad(message_bytes, target_length):
    """
    applies PKCS#1 v1.5 padding to a given message.

    :param message_bytes: The message to be padded.
    :type message_bytes: bytes
    :param target_length: The desired length of the padded message.
    :type target_length: int
    :return: The padded message.
    :rtype: bytes
    """

    # Calculate the required padding length
    padding_length = target_length - len(message_bytes) - 3

    if padding_length < 8:
        raise ValueError("Message too long for PKCS#1 v1.5 padding")

    # Generate the padding string (non-zero random bytes)
    padding = os.urandom(padding_length)

    # The padding consists of a leading 0x00 byte, a 0x02 byte, the padding string, and an ending 0x00, 0x00 bytes
    return b'\x00\x02' + padding + b'\x00\x00' + message_bytes


def pkcs1_v1_5_unpad(padded_message_bytes):
    """
    Remove PKCS#1 v1.5 padding from a given padded message.

    :param padded_message_bytes: The padded message.
    :type padded_message_bytes: bytes
    :return: The unpadded message.
    :rtype: bytes
    """

    if len(padded_message_bytes) < 11:
        raise ValueError("PKCS#1 v1.5 padding incorrect")

    # Locate the first zero byte after the 0x02 byte
    zero_index = padded_message_bytes.find(b'\x00\x00', 2)

    if zero_index == -1:
        raise ValueError("PKCS#1 v1.5 padding incorrect")

    # Extract the message part after the zero byte
    message_bytes = padded_message_bytes[zero_index + 2:]

    return message_bytes


def num_encryption(num, pub_key):
    """
    encrypts a given number 'num', using RSA encryption algorithm with 'pub_key'

    :param num: the given number to encrypt, assuming is less than n
    :type num: int
    :param pub_key: the recipient's public key (n, e)
    :type pub_key: tuple[int]
    :return: the encrypted number
    :rtype: int
    """

    n, e = pub_key
    if num >= n:
        raise Exception(f"The given number is too big. It should be less than {n}")

    return my_utilities.montgomery_ladder(num, e, n)  # num^e (mod n)


def num_decryption(num, private_key):
    """
    decrypts a given number 'num', using RSA decryption algorithm with 'private_key'

    :param num: the given number to decrypt, assuming is less than n
    :type num: int
    :param private_key: the recipient's private key (n, d)
    :type private_key: tuple[int]
    :return: the decrypted number
    :rtype: int
    """

    n, d = private_key

    if num >= n:
        raise Exception(f"The given number is too big. It should be less than {n}")

    return my_utilities.montgomery_ladder(num, d, n)  # num^d (mod n)


def encrypt(msg, pub_key):
    """
    encrypts a message using RSA encryption with PKCS#1 v1.5 padding.

    :param msg: the given message to be encrypted.
    :type msg: str
    :param pub_key: recipient's public key (n, e).
                    not that the function won't work well for small n because of the padding.
    :type pub_key: tuple[int]
    :return: list of integers representing encrypted blocks of the message.
    :rtype: list[int]
    """
    # Unpack the recipient's public key
    n, e = pub_key  # Modulus, Public exponent

    # Convert the message to bytes
    msg_bytes = msg.encode('utf-8')

    # Determine the block size based on the modulus size (in bytes)
    block_size = (n.bit_length() + 7) // 8 - 1  # round to nearest byte, subtract 1 to ensure block is smaller than n
    # Encrypt each block of the message using RSA num_encryption
    encrypted_blocks = []
    for i in range(0, len(msg_bytes), block_size - 11):  # Subtract 11 for padding
        block = msg_bytes[i:i + block_size - 11]
        padded_block = pkcs1_v1_5_pad(block, block_size)
        block_int = int.from_bytes(padded_block, byteorder='big')  # using big-endian method
        encrypted_block = num_encryption(block_int, pub_key)
        encrypted_blocks.append(encrypted_block)
    return encrypted_blocks


def decrypt(encrypted_blocks, private_key):
    """
    decrypts a list of encrypted blocks using RSA decryption with PKCS#1 v1.5 padding.

    :param encrypted_blocks: list of integers representing encrypted blocks of the message.
    :type encrypted_blocks: list[int]
    :param private_key: recipient's private key (n, d)
    :type private_key: tuple[int]
    :return: The decrypted message.
    :rtype: str
    """

    # Unpack the recipient's private key
    n, d = private_key  # Modulus, Private exponent

    # Decrypt each block and reassemble the original message
    decrypted_blocks = []
    for encrypted_block in encrypted_blocks:
        decrypted_block = num_decryption(encrypted_block, private_key)
        # Convert the decrypted block back to bytes
        padded_block = decrypted_block.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
        message_block = pkcs1_v1_5_unpad(padded_block)
        decrypted_blocks.append(message_block)

    # Concatenate decrypted blocks to form the original message
    original_message_bytes = b''.join(decrypted_blocks)
    original_message = original_message_bytes.decode('utf-8')

    return original_message

