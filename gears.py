#!usr/bin/env python
"""
calculate gears transmission ratio
"""

PRECISION = 2


def main():
    # front = [26, 36, 48]
    front = list(map(lambda x: int(x), "26-36-48".split('-')))
    # rear = [11, 13, 15, 17, 19, 21, 23, 27, 31, 35]
    rear = list(map(lambda x: int(x), "11-13-15-17-19-21-23-26-30-34".split('-')))
    rates = {}
    k: int
    for k in front:
        i: int
        for i in rear:
            rate = round(k / i, PRECISION)
            
            if rate not in rates:
                rates[rate] = []
            rates[rate].append((front.index(k)+1, rear.index(i)+1))

    for k in sorted(rates):
        print("{}: {}".format(k, rates[k]))


if __name__ == '__main__':
    main()
