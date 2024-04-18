import numpy as np
from copy import deepcopy

# zeros = np.zeros(5)

# print(zeros)

# a = 1

# for idx, zero in enumerate(zeros):
#     zeros[idx] = a

# a=2
# print(zeros)


class V:
    def __init__(self) -> None:
        self.transmit = True

hi = V()

a = hi.transmit

hi.transmit = False

a= hi.transmit

print(a)