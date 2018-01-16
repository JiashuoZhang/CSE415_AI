from random import *
import math

def run_Guess_My_Number():
    n = randint(0, 1000)
    print(n)
    t = 0
    print("I have a secret number n.")
    print("You can Ask, Guess, or Quit!")

    while True:
        option = input("Ask, Guess, or Quit? ")
        t = t + 1
        if option == "Quit":
            print("Score: 0")
            break
        elif option == "Ask":
            print("If we subtract k from n, is the result divisible by m?")
            k = int(input("k? "))
            m = int(input("m? "))
            print(is_n_minus_k_divisible_by_m(n, k, m))
        elif option == "Guess":
            gString = input("What's your guess? ")
            g = int(gString)
            if g == n:
                print("Score: " + str(math.ceil(n / t)))
                break

def isPrimeUnder1000(m):
    return m > 1 and m < 1000 and all(m % i for i in range(2, m))

def is_n_minus_k_divisible_by_m(n, k, m):
    if not isPrimeUnder1000(m):
        return False
    return (n - k) % m == 0

if __name__ == '__main__':
    run_Guess_My_Number()