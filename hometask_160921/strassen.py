import numpy as np
import sys
import re

def dotStrassen(mat1, mat2):
    if (mat1.shape[0] == 1):
        return np.array([[mat1[0, 0]*mat2[0, 0]]])
    mid = mat1.shape[0] // 2;
    A11 = mat1[:mid, :mid]
    A12 = mat1[:mid, mid:]
    A21 = mat1[mid:, :mid]
    A22 = mat1[mid:, mid:]
    B11 = mat2[:mid, :mid]
    B12 = mat2[:mid, mid:]
    B21 = mat2[mid:, :mid]
    B22 = mat2[mid:, mid:]
    res1 = dotStrassen(A11+A22,B11+B22)
    res2 = dotStrassen(A21+A22, B11)
    res3 = dotStrassen(A11, B12-B22)
    res4 = dotStrassen(A22, B21-B11)
    res5 = dotStrassen(A11+A12, B22)
    res6 = dotStrassen(A21-A11, B11+B12)
    res7 = dotStrassen(A12-A22, B21+B22)
    matres = np.zeros_like(mat1)
    matres[:mid, :mid] = res1+res4-res5+res7
    matres[mid:, :mid] = res2+res4
    matres[:mid, mid:] = res3+res5
    matres[mid:, mid:] = res1+res3-res2+res6
    return matres


if __name__ == "__main__":
    data = np.loadtxt(sys.stdin, dtype = int, ndmin = 2, skiprows = 1)
    n = data.shape[1];
    a1 = data[:n,:]
    a2 = data[n:,:]
    n2 = (1<<(n-1).bit_length())
    mat1 = np.zeros((n2, n2), dtype = int)
    mat1[:n,:n] = a1;
    mat2 = np.zeros((n2, n2), dtype = int)
    mat2[:n,:n] = a2;
    res = dotStrassen(mat1, mat2)[:n, :n]
    print(re.sub(" *[\[\]]", "", np.array_str(res)))
