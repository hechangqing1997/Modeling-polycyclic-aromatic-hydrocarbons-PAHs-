from ann import ANN

from get_data import IAADataset

from torch.utils.data import DataLoader

import torch
import torch.nn as nn
if __name__ == '__main__':
    # sample i
    # input: Measure(SR(parameters[i])) (batchsize,7)
    # output: parameters_predicted[i] (batchsize,8)
    # label : parameters[i]
    # loss : LOSSFUN<parameters_predicted[i],parameters[i]>     LOSSFUN：MSE、MAE、Huber
    # network:
    model=ANN(n_feature=10,n_hidden_layer=50,n_output=9)


    lr=1e-10
    weight_decay=0

    dataset=IAADataset()
    dataloader=DataLoader(dataset,batch_size=8,shuffle=True, num_workers=4)

    device='cuda'
    model.to(device)

    epochs=200
    criterion=nn.MSELoss()
    from logger import Logger
    log=Logger()
    optimizer=torch.optim.SGD([{'params': model.parameters(), 'lr': lr}], lr=lr, momentum=0.9, weight_decay=weight_decay)

    import numpy as np

    # alist=[0.1507, 0.1412, 0.5653, 0.1427, 0.8024, 143, 178]

    loss_list=[]
    for i in range(epochs):
        for j,(x,y) in enumerate(dataloader):
            x = x.to(device)
            y = y.to(device)

            output = model(x)
            # print(y.shape)
            # print(output.shape)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()

            loss_item = loss.detach().cpu().numpy()

            msg=f'epoch: {i}/{epochs} batch:{j}/{len(dataloader)} loss:{loss}'
            log.print_write_log(msg)

            loss_list.append(loss_item)


    # alist = [0.1507, 0.0412, 0.28, 0.0427, 0.8024, 143, 178]
    # # alist=[1.5011947e-01, 3.3587117e-02, 4.5652243e-01, 3.3587117e-02,8.0944782e-01, 1.4463158e+02, 1.7873685e+02]
    # x = torch.FloatTensor(np.array(alist)).to(device)
    # p = model(x)
    # print(p)

    import matplotlib.pyplot as plt

    print(np.array(loss_list))

    plt.plot(np.array(loss_list))
    # plt.figure(dpi=1000, figsize=(20, 4))
    # plt.scatter(_e[:,0],_e[:,1],c=colors[i],label=i,alpha=0.5)
    # plt.legend(numpoints=1)
    plt.savefig('loss.png')

    f=open(f"{lr}.txt", "w")
    for i in range(len(loss_list)):

        msg=f'{i} {loss_list[i]}\n'
        f.write(msg)


