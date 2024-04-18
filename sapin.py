import math
# import numpy as np

h = 0.15
a= 0.05
n_max=8



def horizontal_length(n:int)->float:
    return 2*n*a


def diagonal_length(n:int)->float:
    squared_l = h**2+(horizontal_length(n)-a)**2
    return math.sqrt(squared_l)

def sum_of_lengths(n:int)->float:
    return diagonal_length(n)+horizontal_length(n)

def sum_total(n_max:int)->float:
    #function which sums the horizontal and diagonal lengths from n=1 to n=n_max
    total = 0  
    for n in range(1,n_max+1):
        total += sum_of_lengths(n)
    return total

print(sum_total(n_max))
print(horizontal_length(n_max))
