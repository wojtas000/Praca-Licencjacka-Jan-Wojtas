from random import uniform
import numpy as np

alpha = 0.05
beta = 0.9
gamma = 0.05
d_in = 1
d_out = 1

def znajdz(x, lista):
    sum = 0
    for i in range(len(lista)):
        sum+=lista[i]
        if x< sum:
            return i


liczba_wierzchołków = 1
n = 100000
size = int((alpha + gamma)*n + 1000)

macierz_krawędzi = np.zeros((size,size))
macierz_krawędzi[0,0] = 1
stopnie_in = [1 + d_in]
stopnie_out = [1 + d_out]

mian_in = 1 + d_in
mian_out = 1 + d_out


for i in range(n):
    if i%10000 ==0:
        print(i)
    u1 = uniform(0,1)
    if u1 < alpha:
        u2 = uniform(0,1)
        indeks = znajdz(u2 * mian_in, stopnie_in)
        macierz_krawędzi[liczba_wierzchołków, indeks] +=1
        stopnie_in.append(d_in)
        stopnie_in[indeks] +=1
        stopnie_out.append(1 + d_out)
        mian_in+=1+d_in
        mian_out+= 1 + d_out
        liczba_wierzchołków +=1

    elif u1 < alpha+beta:
        u3, u4 = uniform(0,1), uniform(0,1)
        indeks1 = znajdz(u3 * mian_in, stopnie_in)
        indeks2 = znajdz(u4 * mian_out, stopnie_out)
        macierz_krawędzi[indeks2,indeks1] +=1
        stopnie_in[indeks1] +=1
        stopnie_out[indeks2] +=1
        mian_in += 1
        mian_out += 1

    else:
        u2 = uniform(0, 1)
        indeks = znajdz(u2 * mian_out, stopnie_out)
        macierz_krawędzi[indeks, liczba_wierzchołków] += 1
        stopnie_in.append(1+d_in)
        stopnie_out[indeks] += 1
        stopnie_out.append(d_out)

        mian_in += 1 + d_in
        mian_out += 1 + d_out
        liczba_wierzchołków +=1



suma = 0
for i in range(liczba_wierzchołków):
    for j in range(i+1,liczba_wierzchołków):
        if macierz_krawędzi[i,j] < macierz_krawędzi[j,i]:
            suma+= 2*macierz_krawędzi[i,j]
        else:
            suma += 2*macierz_krawędzi[j,i]

print(suma/n)