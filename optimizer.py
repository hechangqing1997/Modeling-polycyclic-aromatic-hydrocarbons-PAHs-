import random
import numpy as np
from numpy import linalg as LA
import torch
import torch.nn as nn
def sample():
    sample_w = random.uniform(1,4)
    sample_vol = random.uniform(2.5,5.5)
    return np.array([sample_w,sample_vol])

def restrict(samples,water_density,beta):

    result=[]
    for sample in samples:
        sample_density=sample[0]/sample[1]
        if (sample_density-water_density)/water_density<beta:
            # print('save')
            result.append(sample)
        else:
            # print('delete')
            pass
    return result


def compute_loss(samples,gole,water_density,beta):
    # print(restict_samples)
    # print(np.array(restict_samples))
    # print(restict_samples)
    array=torch.from_numpy(np.array(samples)).to(torch.float32)
    # a=torch.mean(array, axis=0)


    # a=torch.mean((array[0] / array[1] - water_density) / water_density)
    print(a)
    p=beta

    print(p)
    loss=p*a

    return loss

class MLP(nn.Module):
    def __init__(self):
        super(MLP,self).__init__()
        self.linear1=nn.Linear(2,4)
        self.simoid1=nn.Sigmoid()
        self.linear2 = nn.Linear(4,1)
        self.simoid2 = nn.Sigmoid()

    def forward(self,x):
        x=self.linear1(x)
        x=self.simoid1(x)
        x=self.linear2(x)
        x=self.simoid2(x)
        return x
if __name__ == '__main__':
    water_weight=2.4
    water_vol=3.7

    gole= torch.from_numpy(np.array([water_weight,water_vol])).to(torch.float32)
    water_density=water_weight/water_vol

    steps=10000
    lr=0.01
    mlp=MLP()
    x=gole

    log_step=100
    optimizer=torch.optim.Adam(mlp.parameters(),lr=lr)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, [int(steps/10), int(steps/2)], 0.5)
    for step in range(steps):

        scheduler.step()
        lr = scheduler.get_lr()

        output=mlp(x)

        samples=[]
        for i in range(10000):
            samples.append(sample())
        # restict_samples = restrict(samples,water_density, output)
        loss=compute_loss(samples,gole,water_density,output)


        loss.backward()

        optimizer.step()

        if step%log_step==0:
            print(f"step {step} lr:{scheduler.get_lr()[0]}  beta:{output} loss:{loss}")


