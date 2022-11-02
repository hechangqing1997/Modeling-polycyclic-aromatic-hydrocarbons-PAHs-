
if __name__ == '__main__':
    from main_SR import SR_and_measure

    ele=[120.5559,  3.2666,  0.5298,  0.7312,  0.1585,  1.2216,  5.6221, 12.2474,0.7069]
    cfg = {}
    cfg['Benzene'] = {'avg_number': ele[0]}
    cfg['Cyclohexane'] = {'avg_number': ele[1]}
    cfg['Pyridine'] = {'avg_number': ele[2]}
    cfg['Furan'] = {'avg_number': ele[3]}
    cfg['Thiophene'] = {'avg_number': ele[4]}
    cfg['Pyrrole'] = {'avg_number': ele[5]}
    cfg['Aliphatic_chain'] = {'avg_number': ele[6], 'avg_length': ele[7]}
    cfg['yafeng'] = {'avg_number': ele[8]}


    SR_and_measure(cfg=cfg)