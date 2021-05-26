import math

## unoptimized sieve of eratosthenes algorithm ##
def sieve(n):
    if n <= 2:
        return {}
    is_prime = [True] * n
    is_prime[0] = False
    yield (is_prime, 0)
    is_prime[1] = False
    yield (is_prime, 1)

    for i in range(2, math.isqrt(n)+1):
        if is_prime[i]:
            is_prime[i] = True
            for j in range(i * i, n, i):
                is_prime[j] = False
                yield (is_prime, i)