import numpy as np
from main_SR import SR_and_measure
from torch.utils.data import Dataset, DataLoader
import torch

def get_structure_param():


    structure_params = [8, 2,0.5,0.5, 2, 0.5, 4, 10,2]
    minus_region = [-2, -1,-0.15,-0.15, -1, -0.15, -1, -2,-1]
    add_region = [2, 1, 0.25, 0.25,1, 0.25, 1, 2,1]
    stride = [0.05, 0.05, 0.05,0.05, 0.05, 0.05, 0.05, 0.05,0.05]

    start_v=[structure_params[i]+minus_region[i] for i in range(len(structure_params))]

    end_v=[structure_params[i]+add_region[i] for i in range(len(structure_params))]

    curren_v=start_v
    while True:
        for i in range(len(structure_params)):
            while abs(curren_v[i]-end_v[i])>1e-2 and (curren_v[i]<=end_v[i]):
                yield curren_v
                curren_v[i]+=stride[i]
        break

def ele2yamldict(ele):

    cfg={}
    cfg['Benzene']={'avg_number':ele[0]}
    cfg['Cyclohexane']={'avg_number':ele[1]}
    cfg['Pyridine'] = {'avg_number': ele[2]}
    cfg['Furan'] = {'avg_number': ele[3]}
    cfg['Thiophene'] = {'avg_number': ele[4]}
    cfg['Pyrrole'] = {'avg_number': ele[5]}
    cfg['Aliphatic_chain'] = {'avg_number': ele[6],'avg_length':ele[7]}
    cfg['yafeng'] = {'avg_number': ele[8]}

    print(round(cfg['Benzene']['avg_number']))
    return cfg

def compute(ele):
    # benzene_num = ele[0]
    # cyclohexane_num = ele[1]
    # pyridine_num = ele[2]
    # furan_num = ele[3]
    # thiophene_num = ele[4]
    # pyrrole_num=ele[5]
    # line_num = ele[6]
    # line_c = ele[7]

    cfg=ele2yamldict(ele)
    result=SR_and_measure(cfg)

    return result


class IAADataset(Dataset):
    def __init__(self,npz_path='data.npz'):
        data=np.load(npz_path)
        self.X=data['X']
        self.Y=data['Y']
        self.current_set_len=self.X.shape[0]
    def __len__(self):
        return self.current_set_len

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]


if __name__ == '__main__':
    #1.Generate n sets of structural parameters

    # Structural parameters: for each core (average number of benzene rings, number of cyclohexanes,
    # number of pyridine rings, number of furans, number of thiophenes, number of pyrroles, number
    # of aliphatic chains, length of aliphatic chains)

    gter=get_structure_param()

    X=[]
    Y=[]
    for ele in gter:
        #2. For each set of structural parameters, 10,000 sets of sr are performed and the final macro parameters are calculated

        micro_parameter=compute(ele)
        print(micro_parameter)
        if micro_parameter:
            X.append( np.array(micro_parameter).astype('float32'))
            Y.append(np.array(ele).astype('float32'))

    X=np.array(X)
    Y=np.array(Y)

    print(X.shape)
    print(Y.shape)
    np.savez('data.npz',X=X,Y=Y)

