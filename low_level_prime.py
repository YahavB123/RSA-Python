def get_n_primes(N):
    """
    computes the first N primes.

    :param N: the amount of first primes to be computed
    :type N: int
    :return: the list of the first N primes
    :rtype: list[int]
    """

    primes = [2]
    cur = 3
    while len(primes) < N:
        for i in range(len(primes)):
            if cur % primes[i] == 0:
                break
        else:
            primes.append(cur)
        cur += 2

    return primes


# generate list:
def main():
    print(get_n_primes(500))


if __name__ == '__main__':
    main()
