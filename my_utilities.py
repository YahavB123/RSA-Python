def montgomery_ladder(x, k, N):
    """
    performs modular exponentiation x^k (mod N) securely and efficiently using the montgomery-ladder method

    :param x: the base
    :type x: int
    :param k: the exponent
    :type k: int
    :param N: the modulus
    :type N: int
    :return: the result: x^k (mod N)
    :rtype: int
    """

    x %= N

    # Initialize two variables to hold the intermediate results
    r0 = 1
    r1 = x

    # Loop through each bit of the binary exponent from most significant to the least significant
    for bit in bin(k)[2:]:
        if bit == '0':
            r1 = (r1 * r0) % N
            r0 = (r0 ** 2) % N
        else:
            r0 = (r0 * r1) % N
            r1 = (r1 ** 2) % N

    # The final result is in r0
    return r0


def mod_inverse(a, m):
    """
    calculates the modular multiplicative inverse of 'a' mod 'm'.
    note that it exists only if 'a', 'm' are coprime.

    :param a: the integer for which to find the modular inverse
    :type a: int
    :param m: the modulus
    :type m: int
    :return: the modular multiplicative inverse of 'a' mod 'm', d: 'a' * 'd' = 1 (mod 'm')
    :rtype: int
    """

    m0, y, x = m, 0, 1

    # Extended Euclidean Algorithm to find modular inverse
    while a > 1:
        q = a // m
        m, a = a % m, m
        y, x = x - q * y, y

    # Ensure x is positive
    return x + m0 if x < 0 else x
