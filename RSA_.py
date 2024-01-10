                                        
                                            # Prince Osei - RSA project

import random


def euclideanAlgorithm(a, b):  # euclidean algorithm
    if b == 0:
        return a

    else:
        return euclideanAlgorithm(b, a % b)


def extendedEuclidean(a, b):        # extended euclidean algorithm
    a, b = max(a, b), min(a, b)

    q = [-1, -1]
    r = [a, b]
    s = [1, 0]
    t = [0, 1]

    while r[-1] > 0:
        q.append(r[-2] // r[-1])
        r.append(r[-2] % r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])

    return t[-2]     # return just the inverse


def millerRabin(n, k):      # miller Rabin Primality Test
    r, s = 0, n - 1

    while s % 2 == 0:       # returns true for all primes and none for non primes
        r += 1
        s //= 2

    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)

        if x == 1 or x == n - 1:
            continue

        for j in range(r - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return

    return True


def generate_prime_number():  # generate large primes using the Miller Rabin Primality

    rounds = 4  # test rounds

    getPrime = random.getrandbits(512)   # initial 512 bits number

    # generates until random 512 bit number is Prime using Miller Rabin
    while not millerRabin(getPrime, rounds):
        getPrime = random.getrandbits(512)
    return getPrime


def modMultiplication(a, b, n):
    return (a * b) % n


def powmod_sm(message, exponent, modulus, group=modMultiplication):   # square and multiply

    result = 1

    while exponent != 0:

        if exponent & 0x1 == 1:  # multiplication
            result = group(result, message, modulus)

        message = group(message, message, modulus)  # squaring
        exponent = exponent >> 1

    return result


def RSAKeyGeneration():
    primeP = generate_prime_number()   # get P
    primeQ = generate_prime_number()    # get q
    n = (primeP * primeQ)                      # get n
    phi_n = (primeP - 1) * (primeQ - 1)          # phi of n
    # print("\n", n)
    # print("phi of n: ", phi_n)

    gen_e = random.randrange(1, (phi_n - 1))     # random generation of e

    # check if gcd(e,phi(n)) = 1 to generate e
    while euclideanAlgorithm(gen_e, phi_n) != 1:        # check if gcd of e is 1
        gen_e = random.randrange(1, (phi_n - 1))
        euclideanAlgorithm(gen_e, phi_n)

    # generate exponent e if gcd is 1
    e = gen_e

    d = extendedEuclidean(e, phi_n)  # generate private key using the EEA

    # return modulus(n), private key(d) and exponent(e)
    return n, e, d


mod, expo, d = RSAKeyGeneration()      # getting values d,e,n
toEncrypt = 200                        # Input message to encrypt

print("K Public (k_pu): n: ", mod, "\n")            # print n
print("K Private (k_pr) : e: ", expo, "\n")         # print e
print("K Private (k_pr) : d: ", d, "\n")            # print private key


# encrypt using square and multiply
cipherText = powmod_sm(toEncrypt, expo, mod)   # encrypt  
print("Cipher Text: ", cipherText, "\n")
plainText = powmod_sm(cipherText, d, mod)      # decrypt using same function
print("Plain Text: ", plainText, "\n")


