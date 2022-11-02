
from scipy.stats import gamma
import matplotlib.pyplot as plt
from benzene import Benzene
import numpy as np
import random

class Sample():
    def __init__(self,method='uniform'):
        self.method=method
        if method=='uniform':
            self.sampler=uniform_sample
        elif method=='gamma':
            self.sampler = gamma_sample
    def __call__(self, a,size,alpha=0.1):
        if self.method=='uniform':
            return self.sampler(a,size,alaph=alpha)
        else:
            return self.sampler(a,size)
    

def gamma_sample(a,size):
    r = gamma.rvs(a=a/2,loc=0,scale=2,size=size)
    # mean, var, skew, kurt = gamma.stats(a, moments='mvsk')
    # print("mean")
    rr=[]
    for ele in r:
        ele=round(ele)
        if ele<0:
            ele=0
        elif ele>2*a:
            ele=2*a
        rr.append(round(ele))
    return rr
def uniform_sample(a,size,alaph):
    
    min_a = a - a * alaph
    max_a = a + a * alaph
    return [round(random.uniform(min_a,max_a)) for i in range(size)]

def sample_molecular(cfg,sample_id,logger):

    sampler=Sample(method='gamma')


    benzene_num=cfg['Benzene']['avg_number']
    cyclohexane_num = cfg['Cyclohexane']['avg_number']
    line_num =cfg['Aliphatic_chain']['avg_number']
    line_c=cfg['Aliphatic_chain']['avg_length']
    furan_num=cfg['Furan']['avg_number']
    thiophene_num = cfg['Thiophene']['avg_number']
    pyrrole_num = cfg['Pyrrole']['avg_number']
    pyridine_num = cfg['Pyridine']['avg_number']
    yafeng_num=cfg['yafeng']['avg_number']

    #随机采样

    ttn=sampler(benzene_num,1)[0]
    if ttn<4:
        ttn=4
    elif ttn>12:
        ttn=12
    sample_benzene_num=ttn

    sample_cyclohexane_num=sampler(cyclohexane_num,1)[0]
    sample_line_num=sampler(line_num,1)[0]
    sample_line_c=sampler(line_c,sample_line_num)
    sample_furan_num=sampler(furan_num,1)[0]
    sample_thiophene_num= sampler(thiophene_num, 1)[0]
    sample_pyrrole_num = sampler(pyrrole_num, 1)[0]
    sample_pyridine_num=sampler(pyridine_num,1)[0]
    sample_yafeng_num = sampler(yafeng_num, 1)[0]

    sample_result=[sample_benzene_num,sample_cyclohexane_num,sample_line_num,sample_line_c,sample_furan_num,sample_thiophene_num,sample_pyrrole_num,sample_pyridine_num,sample_yafeng_num]
    msg=f"Sampling results: Number of benzene rings: {sample_benzene_num} Number of cyclohexanes: {sample_cyclohexane_num} Number of fatty chains: {sample_line_num} \
        Fatty chain length: {sample_line_c} Number of furans: {sample_furan_num} Number of thiophenes: {sample_thiophene_num} Number of pyrroles: {sample_pyrrole_num} Number of pyridines:{sample_pyridine_num} Number of sulfoxides:{ sample_yafeng_num}"
    print(msg)


    #Creation of the first benzene ring and associated initial information
    model = Benzene(benzene_num=sample_benzene_num, file_name=f'./output/{sample_id}.svg')

    #Building a benzene ring core
    for j in range(sample_benzene_num - 1):
        model.add_6ring(ring_type='benzene')

    model.scan()
    #Addition of cyclohexane
    for j in range(sample_cyclohexane_num):
        model.print_structure()
        model.add_6ring(ring_type='cyclohexane')

    #Save txt
    model.save_txt(f'./output/{sample_id}.txt')
    model.print_structure()
    model.get_B_H()
    #model.get_C_num()
    model.save_txt()
    model.get_available_five()

    # Adding a five element heterocyclic ring
    ring5_types=[]
    ring5_types.extend(['furan']*sample_furan_num)
    ring5_types.extend(['thiophene']*sample_thiophene_num)
    ring5_types.extend(['pyrrole']*sample_pyrrole_num)
    random.shuffle(ring5_types)
    for ring_type in ring5_types:
        print(f'add {ring_type}')
        info=model.add_5ring(ring_type=ring_type)
        logger.write_log(info)
    ##Add side chain
    for i in range(sample_line_num):
        info=model.add_line(sample_line_c[i])
        logger.write_log(info)
    ##Add sulfoxide
    for i in range(sample_yafeng_num):
        info=model.add_yafeng()
        logger.write_log(info)

    ##Add pyridine
    for i in range(sample_pyridine_num):
        info=model.add_pyridine()
        logger.write_log(info)
    model.print_structure()
    return sample_result,model



def sample_molecular_part(cfg,sample_id, Adict,logger):
    sampler = Sample(method='gamma')
    line_c = cfg['Aliphatic_chain']['avg_length']

    sample_benzene_num=Adict['benzene_num']
    sample_cyclohexane_num=Adict['cyclohexane_num']
    sample_line_num=Adict['line_num']
    sample_line_c=sampler(line_c,sample_line_num)
    sample_furan_num=Adict['furan_num']
    sample_thiophene_num= Adict['thiophene_num']
    sample_pyrrole_num = Adict['pyrrole_num']
    sample_pyridine_num=Adict['pyridine_num']
    sample_yafeng_num = Adict['yafeng_num']
    sample_result=[sample_benzene_num,sample_cyclohexane_num,sample_line_num,sample_line_c,sample_furan_num,sample_thiophene_num,sample_pyrrole_num,sample_pyridine_num,sample_yafeng_num]
    msg=f"Sampling results: Number of benzene rings: {sample_benzene_num} Number of cyclohexanes: {sample_cyclohexane_num} Number of aliphatic chains: {sample_line_num} \
            Fatty chain length: {sample_line_c} Number of furans: {sample_furan_num} Number of thiophenes: {sample_thiophene_num} Number of pyrroles: {sample_pyrrole_num} Number of pyridines:{sample_pyridine_num} Number of sulfoxides:{ sample_yafeng_num}"
    print(msg)


    #Creation of the first benzene ring and associated initial information
    model = Benzene(benzene_num=sample_benzene_num, file_name=f'./output/{sample_id}.svg')

    #Building a benzene ring core
    for j in range(sample_benzene_num - 1):
        model.add_6ring(ring_type='benzene')

    model.scan()
    #Addition of cyclohexane
    for j in range(sample_cyclohexane_num):
        model.add_6ring(ring_type='cyclohexane')

    #Save txt
    model.save_txt(f'./output/{sample_id}.txt')
    model.print_structure()
    model.get_B_H()

    model.save_txt()
    model.get_available_five()

    # Adding a five element heterocyclic ring
    ring5_types=[]
    ring5_types.extend(['furan']*sample_furan_num)
    ring5_types.extend(['thiophene']*sample_thiophene_num)
    ring5_types.extend(['pyrrole']*sample_pyrrole_num)
    random.shuffle(ring5_types)

    for ring_type in ring5_types:
        print(f'add {ring_type}')
        info=model.add_5ring(ring_type=ring_type)
        logger.write_log(info)
    ##Add side chain
    for i in range(sample_line_num):
        info=model.add_line(sample_line_c[i])
        logger.write_log(info)
    ##Add sulfoxide
    for i in range(sample_yafeng_num):
        info=model.add_yafeng()
        logger.write_log(info)

    ##Add pyridine
    for i in range(sample_pyridine_num):
        info=model.add_pyridine()
        logger.write_log(info)

    model.print_structure()
    return sample_result,model



    