import numpy as np
import pandas as pd
import networkx as nx
import random
import os
import json

def random_subgraphs(graph, k, subgraph_set):
    start_node = random.choice(list(graph.nodes()))
    sampled_nodes = set()
    queue = [(start_node, 0)]

    while queue and len(sampled_nodes) < k:
        node, depth = queue.pop(0)
        if node not in (sampled_nodes | subgraph_set):
            sampled_nodes.add(node)
            neighbors = list(graph.neighbors(node))
            random.shuffle(neighbors)

            # 将邻居节点按照广度优先的顺序添加到队列中
            next_depth = depth + 1

            # 从当前节点的邻居节点中随机选择多个节点（最多选择k个）
            num_neighbors_to_sample = min(k - len(sampled_nodes), len(neighbors))
            num_neighbors_to_sample = int(num_neighbors_to_sample*0.2) + 1
            sampled_neighbors = random.sample(neighbors, num_neighbors_to_sample)
            for neighbor in sampled_neighbors:
                if neighbor not in sampled_nodes:
                    # sampled_nodes.add(neighbor)
                    queue.append((neighbor, next_depth))

    if len(sampled_nodes) < 10:
        sampled_nodes = random_subgraphs(graph, k, subgraph_set)

    return sampled_nodes

def random_paths(subgraph):
    n = int(subgraph.number_of_nodes()/10)
    paths = []
    nodes = list(subgraph.nodes)
    for _ in range(n):
        source = random.choice(nodes)
        target = random.choice(nodes)
        try:
            path = nx.shortest_path(subgraph, source, target)
            while not len(path):
                source = random.choice(nodes)
                target = random.choice(nodes)
                path = nx.shortest_path(subgraph, source, target)
            paths.append(list(path))
            nodes = [node for node in nodes if node not in path]
        except nx.NetworkXNoPath:
            continue
    return paths

subgraph_size = [20, 50, 100, 500]
path_size = [2, 5, 10, 50]

save_path = '../synthetic/'
address_dict_file = '../synthetic/address_dict.csv'
data_path = '../synthetic/badgerdao_concat.csv'

# init address dict
address_dict = {}

if os.path.exists(address_dict_file):
    with open(address_dict_file, 'r') as fp_in:
        for line in fp_in:
            line = line.replace('\n', '')
            addr, index = line.split(',')
            address_dict[addr] = int(index)
        fp_in.close()

# 读取地址交易数据
source_data = pd.read_csv(data_path, header=None)
source_data.columns = ['id', 'start_node','end_node', 'date', 'amount']
source_data = source_data.iloc[:,1:]

# 地址转化为id
source_data_id = source_data.copy()
source_data_id['start_node'] = source_data_id['start_node'].map(address_dict)
source_data_id['end_node'] = source_data_id['end_node'].map(address_dict)


# 创建图G
G = nx.MultiGraph()
G.add_edges_from(source_data_id.iloc[:,:2].values.tolist())
max_cc = G.subgraph(max(list(nx.connected_components(G)), key=len))

# 随机选取子图
n_subgraph = 5
min_size = 20
max_size = 200
subgraph_set = set()
n_size = [random.randint(min_size, max_size) for _ in range(n_subgraph)]
subgraphs_nodes = []
for size in n_size:
    subgraph = random_subgraphs(max_cc, size, subgraph_set)
    print(len(subgraph))
    subgraphs_nodes.append(list(subgraph))
    subgraph_set = subgraph_set | subgraph

# 随机选取边
paths_nodes = []
paths_edges = []
n_paths = 0
for subgraph in subgraphs_nodes:
    paths = random_paths(max_cc.subgraph(subgraph))
    n_paths += len(paths)
    paths_nodes.append(paths)
    for path in paths:
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            paths_edges.append({'start_node':u, 'end_node': v, 'date': '2021-11-30', 'amount':415218125.4817605})
            
paths_edges = pd.DataFrame(paths_edges)
print(len(subgraphs_nodes), n_paths, paths_edges)
# 保存数据
concat_ = pd.concat((source_data_id, paths_edges))
random_data = {'subgraphs':subgraphs_nodes, 'n_subgraphs':len(subgraphs_nodes), 'paths':paths_nodes, 'n_paths':n_paths, 'concat_data':concat_.values.tolist()}

with open(save_path + f'random{n_subgraph}_data.json', 'w') as f:
    json.dump(random_data, f)
