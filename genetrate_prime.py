import random
import my_utilities

# achieved from low_level_prime.py
FIRST500PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                  103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                  211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                  331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                  449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                  587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                  709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                  853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                  991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093,
                  1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223,
                  1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327,
                  1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481,
                  1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
                  1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721,
                  1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867,
                  1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997,
                  1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113,
                  2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267,
                  2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381,
                  2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531,
                  2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671,
                  2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777,
                  2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909,
                  2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061,
                  3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217,
                  3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347,
                  3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499,
                  3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571]


def check_low_level_prime(candidate, lst):
    """
    Checks if a number is divisible by first few primes in lst.

    :param candidate: candidate number
    :type candidate: int
    :param lst: a list of the first few primes
    :type lst: list
    :return: True if the number isn't divisible.
             False if the number is divisible.
    :rtype: bool
    """

    for i in lst:
        if candidate % i == 0 and i ** 2 <= candidate:
            return False
    return True


# ofcourse n is odd, because low_level_prime check has been done
def check_miller_rabin(n, rounds):
    """
    performs the Miller-Rabin probabilistic primality test for n.
    If n is prime, the test will allways return True.
    If n is composite, the test will return False in a probability of 1-4^(-rounds)

    :param n: The prime candidate
    :type n: int
    :param rounds: The amount of round that will be performed on n.
                   The more round, the lower the probability for a prime result for a composite number.
    :type rounds: int
    :return: True if the number is probably prime.
             False if the number is surely composite.
    :rtype: bool
    """

    # Special cases handling
    if n <= 1:
        return False
    if n <= 3:
        return True

    # Find m, k such that: n - 1 = m * 2^k
    m, k = n - 1, 0
    while m % 2 == 0:
        k += 1
        m //= 2

    def surely_composite(a, m1, k1, n1):
        """
        checks if a number is surely composite.
        uses a^(n-1) = a^m1^2^k1 (mod n)  (power tower).

        :param a: the composite candidate.
        :type a: int
        :param m1: odd number, such that n-1 = m1 * 2^k1
        :type m1: int
        :param k1: number, such that n-1= m1* 2^k1
        :type k1: int
        :param n1: the modules
        :type n1: int
        :return: True if the number is surely composite.
                 False if the number is probably prime (in a probability of 0.75)
        :rtype: bool
        """

        x = my_utilities.montgomery_ladder(a, m1, n1)  # a^m1 (mod n), securely and efficiently
        if x == 1 or x == n - 1:  # n-1 is equivalent to -1
            return False  # a doesnt provide evidence about n1 compositeness
        for _ in range(k1):
            x = my_utilities.montgomery_ladder(x, 2, n1)
            if x == 1:
                return True  # x was a none-trivial root of n1
            if x == n - 1:
                return False
        return True

    # Perform the Miller-Rabin test for 'rounds' times:
    for _ in range(rounds):
        a = random.randint(2, n - 2)
        if surely_composite(a, m, k, n):
            return False  # n is not a prime
    return True  # n is prime in a probability of 1 - 4^(-rounds)


def check_prime(n):
    """
    checks the primality of a given number.

    :param n: the given prime candidate
    :type n: int
    :return: True, if the number is prime (with very high probability)
             False, if the number is composite
    :rtype: bool
    """

    # check for low-level prime
    if check_low_level_prime(n, FIRST500PRIMES) is False:
        return False
    # candidate has passed low-level check

    # check for high-level prime
    # rounds is set for 64. The industrial error probability standard is 2^-128
    if check_miller_rabin(n, 64) is False:
        return False

    # candidate has passed all checks and is very likely to be prime
    return True


def get_prime(bits):
    """
    generates a high probability prime number of n bits

    :param bits: the amount of bits in the number
    :type bits: int
    :return: the high probability prime number.
    :rtype: int
    """

    candidate = random.getrandbits(bits)
    while check_prime(candidate) is False:
        candidate = random.getrandbits(bits)

    return candidate
