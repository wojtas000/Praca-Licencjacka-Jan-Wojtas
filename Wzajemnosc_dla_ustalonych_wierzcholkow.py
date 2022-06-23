from random import uniform
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# Celem tej symulacji jest empiryczne wyznaczenie rozkładów zmiennych losowych Xi_v^{out}, Xi_w^{in} (Na podstawie lematu 2.3 artykuł)
# Oraz weryfikacja Theorem 3.1 (artykuł)

alpha = 0.05
beta = 0.9
gamma = 0.05
d_in = 2
d_out = 2

# c_1 + c_2 > 1
c_1 = (alpha + beta)/(1 + d_in * (1 - beta))
c_2 = (gamma + beta)/(1 + d_out * (1 - beta))

v = 3
w = 8
n = 100000
probs = [alpha, alpha+beta, 1]



v_out_val = []  # stopień out wierzchołka v
w_in_val = []    # stopień in wierzchołka w
vw_distribution = []  #iloczyn stopni wierzchołków v_{out} i w_{in}
vw_edges_val = [] # liczba krawędzi z wierzchołka v do w
m = 10000

for j in range(m):
    vw_edges = 0
    node_number = 1
    v_out = 0
    w_in = 0

    for i in range(1,n+1):

        rand = uniform(0,1)

        if rand < probs[0]:
            node_number += 1
            r_w = uniform(0, 1)
            if w >= node_number and r_w < (w_in + d_in) / (i + 1 + d_in * node_number):
                w_in += 1
                if node_number == v:
                    v_out += 1
                    vw_edges += 1
            else:
                if node_number == v:
                    v_out += 1

        elif rand < probs[1]:
            r_v = uniform(0, 1)
            r_w = uniform(0, 1)
            if node_number >= v:
                if r_v < (v_out + d_out)/(i+1+ d_out*node_number):
                    v_out += 1
            if node_number >= w:
                if r_w < (w_in + d_in)/(i+1+d_in*node_number):
                    w_in += 1
            if node_number >= v and node_number >= w and  r_v < (v_out + d_out)/(i+1+ d_out*node_number) and r_w < (w_in + d_in)/(i+1+d_in*node_number):
                vw_edges +=1

        else:
            node_number+=1
            r_v = uniform(0,1)
            if v >= node_number and r_v < (v_out + d_out)/(i+1+ d_out*node_number):
                v_out+=1
                if node_number ==w:
                    w_in +=1
                    vw_edges+=1
            else:
                if node_number ==w:
                    w_in +=1

    v_out_val.append(v_out)
    w_in_val.append(w_in)
    vw_distribution.append(v_out*w_in)
    vw_edges_val.append(vw_edges)

print(v_out_val)
print(w_in_val)

v_out_val = np.array(v_out_val) / (n**c_2)
w_in_val = np.array(w_in_val) / (n**c_1)
vw_distribution = np.array(vw_distribution) / (n**(c_2+c_1))
vw_edges_val = np.array(vw_edges_val) / (n**(c_2+c_1-1))


# Generowanie wykresów

lista = [v_out_val, w_in_val, vw_distribution, vw_edges_val]
titles = ['D_v^{out}/n^{c_2}', 'D_w^{in}/n^{c_1}', 'D_w^{in}*D_v^{out}/n^{c_2+c_1}', 'L(i,j)/n^{c_1+c_2-1}']
for j in range(len(lista)):
    plt.figure(figsize = (14,7))
    plt.style.use('seaborn-whitegrid')
    k, bins, patches = plt.hist(lista[j], bins = 40, edgecolor = '#000000')
    k = k.astype('int')
    for i in range(len(patches)):
        patches[i].set_facecolor(plt.cm.viridis(k[i] / max(k)))
    plt.title('Histogram' + titles[j])
    plt.show()
