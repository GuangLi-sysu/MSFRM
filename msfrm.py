import numpy as np
import pickle as pickle
from tqdm import tqdm
import sparse as sp
import pandas as pd

def tensor2lil(tensor, shape=None):
    value = tensor.iloc[:, -1]
    attr = tensor.iloc[:, :-1]
    stensor = sp.COO(attr.to_numpy().T, value.to_numpy().T, shape=shape)
    sparse_matrix = stensor.to_scipy_sparse().asformat('coo')
    sparse_matrix = sparse_matrix.asfptype()
    M = sparse_matrix.copy().tolil()
    return M

# choose next hop flow
def choosepath(node, M, weight_list, path_list):
    row_ind = M.rows[node]
    row_weight = weight_list[row_ind]
    id_wei = zip(row_ind, row_weight)
    id_wei = sorted(id_wei, key=lambda x: x[1])

    for (id, weight) in id_wei[::-1]:
        # skip ring
        path = path_list[id]
        if node in path:
            continue
        
        # skip none node
        if path[-1] == -1:
            continue

        if weight == 0:
            continue

        return id

    return 0

def initmatrix(tensor):
    m = max(max(tensor['from']), max(tensor['to'])) + 1
    M_weight = tensor2lil(tensor, (m,m))
    M = M_weight.multiply(M_weight.power(-1))
    M = M.tolil()

    # initialize: eliminate self-loop
    for i in range(m):
        M[i, i] = 0
        M_weight[i, i] = 0

    return M, M_weight

# initialize: lists of flows and weights
def initweight(M_weight):
    weight_list = []
    path_list = []

    for i, (nodes, node_data) in enumerate(zip(M_weight.rows, M_weight.data)):
        if not nodes:
            weight_list.append(0)
            path_list.append([-1])
            continue
        
        max_ind = np.argmax(node_data)
        max_weight = node_data[max_ind]
        max_ind = nodes[max_ind]
        if max_weight:
            weight_list.append(max_weight/2)
            path_list.append([i, max_ind])
        else:
            weight_list.append(0)
            path_list.append([-1])
    return weight_list, path_list

def get_top_path(path_list, n=100):
    path_list = sorted(path_list, key=lambda x: x[0], reverse=True)
    nodeset = []
    top_path = []

    for score, path in path_list:
        if len(top_path) == n:
            break
        if set(path)&set(nodeset):
            continue
        else:
            top_path.append((score, path))
            nodeset += path
    return top_path

def msfrm(tensor, k):
    M, M_weight = initmatrix(tensor)
    weight_list, path_list = initweight(M_weight)

    iters = 2
    best_ind = np.argmax(weight_list)
    bestscore = weight_list[best_ind] / 2
    best_flow = path_list[best_ind]
    print('Weight vector initializing successful! Max score is %f, subgraph is %s.'%(bestscore, str(path_list[best_ind])))
    nodes_list = list(np.where(np.array(weight_list) > 0)[0])
    weight_list = np.array(weight_list)

    # sorted flows by weights and get top k flows
    score_list = np.array(weight_list/iters)
    top_path = get_top_path(list(zip(score_list, path_list)), k)
    iters += 1

    while nodes_list:
        cur_weight = []
        cur_path = []
        for node in nodes_list:
            if path_list[node][-1] == -1:
                continue

            node_id = choosepath(node, M, weight_list, path_list)

            if node_id == 0:
                cur_path.append((node, path_list[node] + [-1]))
                cur_weight.append((node, 0))
                continue
            
            cur_path.append((node, [node] + path_list[node_id]))
            cur_weight.append((node, (weight_list[node_id] + M_weight[node, node_id])))

        # update list of weights
        for (node, weight) in cur_weight:
            weight_list[node] = weight

        # update list of flows
        for (node, path) in cur_path:
            path_list[node] = path

        # prune operator
        nodes_list = list(np.where(np.array(weight_list) > 0)[0])
        best_ind = np.argmax(weight_list)
        cur_score = weight_list[best_ind] / iters
        cur_path = path_list[best_ind]
        
        if bestscore < cur_score:
            bestscore = cur_score
            best_flow = cur_path
            print('!!!!!!!!!!!!!!\n')
            print('Max score update: %f! Flow is %s.'%(bestscore, str(best_flow)))

        score_list = np.array(weight_list/iters)
        if len(nodes_list):
            top_path = get_top_path(top_path + list(zip(score_list, path_list)), k)

        iters += 1
        # print(f'Iter:{iters}, Score:{cur_score}, Node list length: {len(nodes_list)}, Current node: {best_ind}, Path length:{len(cur_path)}, Path: {cur_path[-5:]}')

    return top_path