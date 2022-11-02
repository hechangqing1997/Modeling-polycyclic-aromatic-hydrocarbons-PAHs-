from ann import ANN
import  numpy as np

class IAA():
    def __init__(self):
        self.network=self.init_network()
        pass
    def measurement(self,average_MW,carbon,hydrogen,sulfur,nitrogen,oxygen,hydrogen_type_1_aromatic,hydrogen_type_2_α_ch_ch2,hydrogen_type_3_α_ch3,hydrogen_type_4_β_ch2,hydrogen_type_5_β_ch3,hydrogen_type_6_γ_ch3):
        pass

    def init_network(self,n_feature=12, n_hidden_layer=35, n_output=13):
        network=ANN(n_feature, n_hidden_layer, n_output)
        return  network
    def compute_OFV(self,pv_exp,pv_pred):

        x=(pv_exp-pv_pred)/pv_exp
        print(x)
        x=np.linalg.norm(x, ord=2,axis=0,keepdims=True)
        return x
    def stochastic_econstruction(self,parameter):

        pass
    def test(self):
        pv_exp=np.array([2,3,4,5])
        pv_pred=np.array([2,3,4,7])
        print(self.compute_OFV(pv_exp,pv_pred))
        pass
if __name__ == '__main__':
    model=IAA()
    model.test()