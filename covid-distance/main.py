#!/usr/bin/en python
from math import sqrt

from scipy.spatial import distance

a = (0, 0, 0)
b = (1, 0, 0)
c = (1/2, sqrt(3)/2, 0)
d = (1/2, 1/(2*sqrt(3)), -sqrt(2/3))

print(f"a->b: {distance.euclidean(a, b)}")
print(f"a->c: {distance.euclidean(a, c)}")
print(f"a->d: {distance.euclidean(a, d)}")
print(f"b->c: {distance.euclidean(b, c)}")
print(f"b->d: {distance.euclidean(b, d)}")
print(f"c->d: {distance.euclidean(c, d)}")
