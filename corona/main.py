
infected = [
    
]


def sum_geom(b=1, q=1.115, n=100):
    return b*(1-pow(q, n))/(1-q)


if __name__ == '__main__':
    [print(f'{x:3d} {int(pow(1.1, x)):15.6g} {int(sum_geom(n=x)):15.6g}') for x in range(0, 200, 1)]
    # print(main())
