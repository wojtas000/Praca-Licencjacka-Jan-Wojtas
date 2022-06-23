from numpy.random import choice
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pyvis.network

class Network:
    def __init__(self, alpha: float, beta: float, gamma: float, d_in: float, d_out: float):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.d_in = d_in
        self.d_out = d_out
        self.degree = [[1, 1]]
        self.edge_from = [0]
        self.edge_to = [0]
        self.time = 0
        self.length = 1
        self.edge_dict = {(0,0): 1}
        self.c1 = (self.alpha + self.beta) / (1 + self.d_in * (1 - self.beta))
        self.c2 = (self.gamma + self.beta) / (1 + self.d_out * (1 - self.beta))

    def prob_check(self):
        if self.alpha + self.beta + self.gamma != 1:
            raise ValueError('parameters do not sum up to 1')
        else:
            pass

    def choose_scheme(self):
        schemes = [1, 2, 3]
        draw = choice(schemes, 1, p=[self.alpha, self.beta, self.gamma])
        return draw

    def alpha_scheme(self):

        probs = []
        for i in range(self.length):
            prob = (self.degree[i][0] + self.d_in) / (self.time + 1 + self.d_in * self.length)
            probs.append(prob)

        draw = int(choice(list(range(self.length)), 1, p=probs))

        self.edge_from.append(self.length)
        self.edge_to.append(draw)
        self.degree[draw][0] += 1
        self.edge_dict[(self.length, draw)] = 1
        self.degree.append([0, 1])
        self.length += 1
        self.time += 1

    def beta_scheme(self):
        vertex_list = []
        probs = []
        for i in range(self.length):
            for j in range(self.length):
                vertex_list.append([i, j])
                prob = ((self.degree[j][0] + self.d_in) / (self.time + 1 + self.d_in * self.length)) * (
                            (self.degree[i][1] + self.d_out) / (self.time + 1 + self.d_out * self.length))
                probs.append(prob)

        draw_idx = int(choice(len(vertex_list), 1, p=probs))
        draw = vertex_list[draw_idx]
        self.edge_from.append(draw[0])
        self.edge_to.append(draw[1])
        self.degree[draw[0]][1] += 1
        self.degree[draw[1]][0] += 1
        self.time += 1
        try:
            self.edge_dict[(draw[0], draw[1])] += 1
        except:
            self.edge_dict[(draw[0], draw[1])] = 1
    def gamma_scheme(self):

        probs = []
        for i in range(self.length):
            prob = (self.degree[i][1] + self.d_out) / (self.time + 1 + self.d_out * self.length)
            probs.append(prob)

        draw = int(choice(list(range(self.length)), 1, p=probs))

        self.edge_from.append(draw)
        self.edge_to.append(self.length)
        self.edge_dict[(draw,self.length)] = 1
        self.degree[draw][1] += 1
        self.degree.append([1, 0])
        self.length += 1
        self.time += 1


    def get_number_of_reciprocal_edges(self,node1,node2):
        return min(self.edge_dict[(node1,node2)],self.edge_dict[(node2,node1)])

    def reciprocity_coefficient(self):
        R = 0
        for j in range(1,self.length):
            for i in range(j):
                try:
                    R += min(self.edge_dict[(i,j)],self.edge_dict[(j,i)])
                except:
                    continue
        return R * 2/(self.time + 1)

    def network_evolution(self, evolution_time = 100):
        for i in range(evolution_time):
            scheme = Net.choose_scheme()
            if scheme == 1:
                Net.alpha_scheme()
            elif scheme == 2:
                Net.beta_scheme()
            else:
                Net.gamma_scheme()

def barplot(x,y):
    y_pos = np.arange(len(x))
    plt.bar(y_pos, y)
    plt.xticks(y_pos, x)
    plt.show()

def visualise_network(Net: Network, highlited_node = None):
    global img_num
    df = pd.DataFrame({'from': Net.edge_from, 'to': Net.edge_to})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())

    degrees = dict(G.degree)


    nx.set_node_attributes(G, degrees, 'size')

    net = pyvis.network.Network(height='1000px', width='1000px', bgcolor='#222222', font_color='white', notebook = True, directed=True)
    net.from_nx(G)

    neighbor_map = net.get_adj_list()
    i = 0
    for node in net.nodes:
        if node['id'] == highlited_node:
            node['color'] = 'red'
        node['title'] = ' Sąsiedzi:' + ''.join(str(neighbor_map[node['id']]))
        node['size'] = degrees[i]
        # node['shape'] = 'circle'
        i+=1
    net.show_buttons(filter_=['physics'])
    net.set_edge_smooth('dynamic')
    net.show(f'NetworkImage{img_num}.html')
    img_num+=1



if __name__ == '__main__':
    highlighted_node = 17
    img_num = 1
    Net = Network(0.05, 0.9, 0.05, 5, 5)
    Net.prob_check()
    time = 5000
    Net.network_evolution(evolution_time = time)
    visualise_network(Net = Net, highlited_node=None )


