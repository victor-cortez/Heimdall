import numpy as np
a = np.random.randint(16, size=(4,4)).astype('uint8')
b = np.random.randint(16, size=(4,4)).astype('uint8')
print(a)
print(b)
print(np.dot(a,b))