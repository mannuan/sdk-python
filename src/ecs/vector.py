# -*- coding:utf-8 -*-

from math import sqrt

class Vector:
    """
    A Vector is a 3-tuple of (x,y,z) coordinates.
    """
    def __init__(self,x,y,z):
        self._x = x
        self._y = y
        self._z = z
    def __repr__(self):
        return '{%.3g} ,{%.3g} ,{%.3g}'%(self._x, self._y, self._z)
    def __str__(self):
        return '({},{},{})'.format(self._x, self._y, self._z)
    def __add__(self,other):
        return Vector(self._x + other._x, self._y + other._y, self._z + other._z)
    def __sub__(self,other):
        return Vector(self._x - other._x, self._y - other._y, self._z - other._z)
    def norm(self):
        result = sqrt(self._x**2 + self._y**2 + self._z**2)
        return result
    def __mul__(self,other):
        return Vector(self._x * other, self * other, self._z * other)
    def x(self):
        return self._x
    def y(self):
        return self._y
    def z(self):
        return self._z
    def clear(self):
        return Vector(0 ,0 ,0)

    def __eq__(self, a):
        return self._x == a._x and self._y == a._y and self._z == a._z