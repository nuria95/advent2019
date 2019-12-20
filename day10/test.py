from collections import namedtuple
myTuple = namedtuple("Test", ['a', 'b', 'c', 'd'])
records = [myTuple(3, 2, 1, 4), myTuple(5, 6, 7, 8)]
print(records)
print([[record.a, record.b] for record in records if record.c == 1])


p=[2,3,4,5,6]
m=[5,6]
print(p-m)