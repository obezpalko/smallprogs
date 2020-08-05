
import cProfile
import math


def sum_digits(number):
    pass


def split_to_digits_num(number):
    return [(number//(10**i)) % 10 for i in range(math.ceil(math.log(number, 10))-1, -1, -1)]


def split_to_digits_str(number):
    return [int(d) for d in str(number)]


def main():
    n = 12345678901234567890
    setup = "from __main__ import split_to_digits_num, split_to_digits_str"
    # print(timeit.timeit(f"split_to_digits_num({n})", setup=setup))
    # print(timeit.timeit(f"split_to_digits_str({n})", setup=setup))
    cProfile.run(f"split_to_digits_str({n})")
    cProfile.run(f"split_to_digits_num({n})")


if __name__ == '__main__':
    main()
