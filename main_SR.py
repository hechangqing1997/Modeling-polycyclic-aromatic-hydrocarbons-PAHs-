from cgi import print_form
from http.client import NON_AUTHORITATIVE_INFORMATION
from turtle import ht
from typing import Final
from benzene import Benzene
from sample import sample_molecular
from sample import sample_molecular_part
from config import read_config_file
import numpy as np
import yaml
import random


def get_H(num_H, num_B_H, result):
    num = 0
    i = result[2]
    for j in range(0, i):
        num += result[3][j] * 2
    num = num + num_H + num_B_H + result[7] * 3
    return num


def get_bh(result):
    num = 0
    i = result[2]
    for i in range(0, i):
        num += result[3][i] - 2
    return num


def get_C(result):
    num = 0
    i = result[2]
    num += result[1] * 4
    for j in range(0, i):
        num += result[3][j]
    num = num + result[4] * 2 + result[5] * 2 + result[6] * 2 + result[7] * 5
    return num


def SR_and_measure(cfg):

    from logger import Logger
    log=Logger()
    # cfg = read_config_file('./config/example1.yml')
    result1 = []  ##list for island 1
    result2 = []  ##list for island 2
    SR_result = []

    exp_num=100
    for i in range(1, exp_num+1):

        log.write_log(f'————————————————————-')
        log.write_log(f'Try to build the {i} molecule')
        try:
            log.write_log('Start of the first part of the modelling')
            result_list1 = []

            sample_result1, model1 = sample_molecular(cfg, sample_id=i,logger=log)
            print(cfg)
            result1.append(sample_result1)
            num_B_H = model1.get_B_H()
            num_H = model1.get_H()  ## Hydrogen number of cyclohexane
            num = get_H(num_B_H, num_H, sample_result1)
            bh = get_bh(sample_result1)
            C = model1.get_C_num()
            D = get_C(sample_result1)
            print("The number of hydrogens on the aromatic hydrocarbons :" + str(num_B_H))
            print("Total hydrogen number:" + str(num))
            print("a-hydrogen number:" + str(sample_result1[2]))
            print("b-hydrogen number:" + str(bh))
            print("r-hydrogen number:" + str(sample_result1[2]))
            print("oxygen number:" + str(sample_result1[8] + sample_result1[4]))
            print("sulfur number:" + str(sample_result1[8] + sample_result1[1]))
            print("nitrogen number:" + str(sample_result1[6] + sample_result1[7]))
            print("Total carbon number:" + str(C + D))
            total_atom1 = num + (sample_result1[8] + sample_result1[4]) + (sample_result1[8] + sample_result1[1]) + (
                        sample_result1[6] + sample_result1[7]) + (C + D)
            print(f"Total atomic number：{total_atom1}")
            result_list1.append(num_B_H)
            result_list1.append(num)
            result_list1.append(sample_result1[2])
            result_list1.append(bh)
            result_list1.append(sample_result1[2])
            result_list1.append((C + D))
            result_list1.append(total_atom1)  # 7.总原子数
            result_list1.append((sample_result1[6] + sample_result1[7]))  # 8.氮原子数
            result_list1.append((sample_result1[8] + sample_result1[5]))  # 9.硫原子数
            result_list1.append((sample_result1[8] + sample_result1[4]))  # 10.氧原子数

            # left1 = 16 - result1[i - 1][0]
            # left2 = 4 - result1[i - 1][1]


            #第二部分建模

            log.write_log('Start of the second part of the modelling')
            Adict={}
            Adict['benzene_num']=round(2*cfg['Benzene']['avg_number']-sample_result1[0])
            Adict['cyclohexane_num']=round(2*cfg['Cyclohexane']['avg_number']-sample_result1[1])
            Adict['line_num']=round(2*cfg['Aliphatic_chain']['avg_number']-sample_result1[2])
            Adict['furan_num']=round(2*cfg['Furan']['avg_number']-sample_result1[4])
            Adict['thiophene_num']=round(2*cfg['Thiophene']['avg_number']-sample_result1[5])
            Adict['pyrrole_num']=round(2*cfg['Pyrrole']['avg_number']-sample_result1[6])
            Adict['pyridine_num']=round(2*cfg['Pyridine']['avg_number']-sample_result1[7])
            Adict['yafeng_num']=round(2*cfg['yafeng']['avg_number']-sample_result1[8])
            if 1:
                result_list2 = []
                sample_result2, model2 = sample_molecular_part(cfg, i + 100,Adict,logger=log)
                result2.append(sample_result2)
                num_B_H = model2.get_B_H()
                num_H = model2.get_H()  ## 环己烷的氢数
                num = get_H(num_B_H, num_H, sample_result2)
                bh = get_bh(sample_result2)
                C = model2.get_C_num()
                D = get_C(sample_result2)
                print("The number of hydrogens on the aromatic hydrocarbons :" + str(num_B_H))
                print("Total hydrogen number:" + str(num))
                print("a-hydrogen number:" + str(sample_result2[2]))
                print("b-hydrogen number:" + str(bh))
                print("r-hydrogen number:"  + str(sample_result2[2]))
                print("oxygen number:" + str(sample_result2[8] + sample_result2[4]))
                print("sulfur number:" + str(sample_result2[8] + sample_result2[5]))
                print("nitrogen number:" + str(sample_result2[6] + sample_result2[7]))
                print("Total carbon number:" + str(C + D))
                total_atom2 = num + (sample_result2[8] + sample_result2[4]) + (
                            sample_result2[8] + sample_result2[1]) + (sample_result2[6] + sample_result2[7]) + (C + D)
                print(f"Total atomic number：{total_atom2}")

                result_list2.append(num_B_H)
                result_list2.append(num)
                result_list2.append(sample_result2[2])
                result_list2.append(bh)
                result_list2.append(sample_result2[2])
                result_list2.append((C + D))
                result_list2.append(total_atom2)  # 6.总原子数
                result_list2.append((sample_result2[6] + sample_result2[7]))  # 7.氮原子数
                result_list2.append((sample_result2[8] + sample_result2[5]))  # 8.硫原子数
                result_list2.append((sample_result2[8] + sample_result2[4]))  # 9.氧原子数
            haha = []
            for j in range(0, 10):
                haha.append(result_list1[j] + result_list2[j])


            gaga = []
            gaga.append(haha[0] / haha[1])  # 芳香氢比例
            gaga.append(haha[2] / haha[1])  # aH
            gaga.append(haha[3] / haha[1])  # bH
            gaga.append(haha[2] / haha[1])  # rH
            gaga.append(haha[5] / haha[1])  # C/H
            gaga.append(haha[5])  # CT
            gaga.append(haha[1]-10)  # CH
            gaga.append((haha[7]) / (haha[6]+2))
            gaga.append(haha[8] / (haha[6]+2))
            gaga.append((haha[9]+12) / (haha[6]+2))

            SR_result.append(gaga)

            log.write_log(f'Attempt to build the {i}th molecule succeeds')


        except:

            log.write_log(f'Failed attempt to build the {i}th molecule')
            continue

        # else:
        # result1.remove(sample_result1)

        # num_C = model1.get_C_num()

    # print(SR_result)
        print(f'Total atomic number:{haha[6] + 2}')
    if len(SR_result) == 0:
        return None

    h1 = 0
    h2 = 0
    h3 = 0
    h4 = 0
    h5 = 0
    h6 = 0
    h7 = 0
    h8 = 0
    h9 = 0
    h10 = 0

    for i in range(len(SR_result)):
        h1 += SR_result[i][0]
        h2 += SR_result[i][1]
        h3 += SR_result[i][2]
        h4 += SR_result[i][3]
        h5 += SR_result[i][4]
        h6 += SR_result[i][5]
        h7 += SR_result[i][6]
        h8 += SR_result[i][7]
        h9 += SR_result[i][8]
        h10 += SR_result[i][9]
    final_result = []
    final_result.append(h1 / len(SR_result))
    final_result.append(h2 / len(SR_result))
    final_result.append(h3 / len(SR_result))
    final_result.append(h4 / len(SR_result))
    final_result.append(h5 / len(SR_result))
    final_result.append(h6 / len(SR_result))
    final_result.append(h7 / len(SR_result))
    final_result.append((h8 / len(SR_result))*100)
    final_result.append((h9 / len(SR_result))*100)
    final_result.append((h10 / len(SR_result))*100)
    print(final_result)


    print(f'accept rate:{len(SR_result)/exp_num}')
    return final_result


if __name__ == '__main__':
    cfg = read_config_file('./config/example1.yml')
    SR_and_measure(cfg)
    pass