N = 100

C = np.zeros([N,N],float)
for i in range(N):
    for j in range(N):
        for k in range(N):
            C[i,j]+= A[i,k]*B[k,j]

print(C)
""" 
for N = 1000, this is 2 billion operations
for N = 2000, this is 16 billion operations

2N**3 is the amount of operations

this is why it is harder to have matrices larger than 1000x1000"""

