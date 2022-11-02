import numpy as np


from svg_parser_master.generate_svg import Generate_svg
from class_ben import  ben
from line import  C_Line
from ring5 import Ring5
from cyclohexane import Cyclohexane
import random

class Benzene():
    def __init__(self,N=41,benzene_num=13,length_x=3000,length_y=3000,a=100,file_name='tmp.svg'):
        self.N=N
        self.benzene_num=benzene_num
        self.a=np.zeros((self.N,self.N),dtype='int')
        self.a.fill(-1)
        self.center_x=int((self.N - 1) / 2)
        self.center_y =self.center_x
        self.benzene_cnt=0
        self.hasBenzeneRow = np.zeros(self.N)
        self.sx=-1
        self.ex=-1  
        self.posible_6ring=[]
        self.ben_class_list = []

        self.ben_list=[]
        self.available_cyclohexane_list=[]

        self.cyclohexane_list=[]
        self.cyclohexane_cnt=0
        self.ring5_list=[]


        self.B_H=0 #This refers to the number of H's on the benzene ring
        self.H= 0
        self.C_num = 0 #This represents the total number of C
        self.hash_list = [] #This is a hash table
        self.available_five_list = []
        self.available_line = []
        self.double_C = 0
        self.triple_C = 0
        self.add_init_benzene()

        self.g=Generate_svg(length_x,length_y,a,file_name)

        self.lines_list=[]
    def add_init_benzene(self):
        x=self.center_x
        y=self.center_y

        self.a[x,y]=1
        self.benzene_cnt+=1
        self.ben_list.append((x,y))

        self.hasBenzeneRow[x]=1
        self.sx=x
        self.ex=x

        self.a[x,y-2]=0
        self.a[x,y+2]=0

        self.a[x-1, y - 1] = 0
        self.a[x-1, y + 1] = 0

        self.a[x + 1, y - 1] = 0
        self.a[x + 1, y + 1] = 0

        self.posible_6ring.append((x,y-2))
        self.posible_6ring.append((x, y+2))
        self.posible_6ring.append((x-1, y - 1))
        self.posible_6ring.append((x-1, y + 1))
        self.posible_6ring.append((x+1, y - 1))
        self.posible_6ring.append((x+1, y + 1))
        ben_huan = ben(10000*x**2 + y**2)
        self.ben_class_list.append(ben_huan)
        self.hash_list.append((10000*x**2 + y**2,0))




    def get_point_list(self,x,y):
        r=[
            (x,y-2),(x,y+2),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)
        ]
        return  r
    def add_atom(self,x,y,ring_type):
        print(f'Set({x},{y}) to {ring_type}')

        if ring_type=='benzene':
            self.a[x][y]=1
            self.benzene_cnt += 1
            self.ben_list.append((x, y))
            ben_cla = ben(10000*x**2 + y**2)
            self.ben_class_list.append(ben_cla)
            self.hash_list.append((10000*x**2 + y**2,0))

            self.sx=min(self.sx,x)
            self.ex = max(self.ex, x)

            p_list=self.get_point_list(x,y)
            for (x,y) in p_list:
                if self.a[x][y]==-1:
                    print('Add possible locations')
                    self.a[x][y]=0
                    self.posible_6ring.append((x,y))
                elif self.a[x][y]==0:
                    # print('Already a possible location')
                    pass
                elif self.a[x][y]==1:
                    # print('Benzene ring already present')
                    pass
        elif ring_type=='cyclohexane':
            self.a[x][y]=2
            self.cyclohexane_cnt += 1
            self.cyclohexane_list.append((x, y))

            self.sx=min(self.sx,x)
            self.ex = max(self.ex, x)


    def add_6ring(self,ring_type):

        if ring_type == 'benzene':
            posible_num=len(self.posible_6ring)
            rand_i=np.random.randint(0,posible_num)
            x,y=self.posible_6ring.pop(rand_i)
            self.add_atom(x,y,ring_type)
        else:
            self.get_available_cyclohexane()
            posible_num = len(self.available_cyclohexane_list)
            rand_i = np.random.randint(0, posible_num)
            x, y, id = self.available_cyclohexane_list[rand_i]
            benhuan = self.get_ben(10000*x**2 + y**2)

            assert benhuan.node[id]==0 and benhuan.node[(id+1)%6]==0,'Error adding cyclohexane'
            benhuan.node[id] = Cyclohexane(x, y, id)
            benhuan.node[(id+1)%6]=-1 #-1表示被与id的碳公用边接环己烷
            print(f"Add cyclohexane to {x} {y} {id}")
            # print('ddd',benhuan.node[id] == 0)

            if id==0:
                x=x-1
                y=y-1
            elif id==1:
                x=x
                y=y-2
            elif id==2:
                x=x+1
                y=y-1
            elif id==3:
                x=x+1
                y=y+1
            elif id == 4:
                x = x
                y = y + 2
            elif id==5:
                x = x-1
                y = y+1
            self.a[x][y] = 2
            self.cyclohexane_cnt += 1
            self.cyclohexane_list.append((x, y))
    def get_available_cyclohexane(self):
        self.available_cyclohexane_list = []
        for (x, y) in self.ben_list:
            benhuan = self.get_ben(10000*x**2 + y**2)
            if benhuan.node[0] == 0 and benhuan.node[1] == 0:
                self.available_cyclohexane_list.append((x, y, 0))
            if benhuan.node[1] == 0 and benhuan.node[2] == 0:
                self.available_cyclohexane_list.append((x, y, 1))
            if benhuan.node[2] == 0 and benhuan.node[3] == 0:
                self.available_cyclohexane_list.append((x, y, 2))
            if benhuan.node[3] == 0 and benhuan.node[4] == 0:
                self.available_cyclohexane_list.append((x, y, 3))
            if benhuan.node[4] == 0 and benhuan.node[5] == 0:
                self.available_cyclohexane_list.append((x, y, 4))
            if benhuan.node[5] == 0 and benhuan.node[0] == 0:
                self.available_cyclohexane_list.append((x, y, 5))
        print(f"list {self.available_cyclohexane_list}")
    def add_5ring(self,ring_type):
        self.print_structure()
        self.get_available_five()
        posible_num=len(self.available_five_list)
        print(posible_num)
        self.print_structure()
        assert posible_num>0,'Failed to add pentacyclic, number of loci is 0'
        rand_i=np.random.randint(0,posible_num)
        x,y,id=self.available_five_list.pop(rand_i)
        
        ##random substitution of position, 1, 4
        qudai_idx=random.choice([1,4])
        # print(qudai_idx)
        self.ring5_list.append((x,y,id,qudai_idx,ring_type))

        benhuan = self.get_ben(10000*x**2 + y**2)
        benhuan.node[id] = Ring5(x, y, id,qudai_idx,ring_type)
        benhuan.node[(id + 1) % 6] = -1  # -1 denotes a carbon common edge-joined five-membered ring with id

        msg=f'Adding the five-membered ring {ring_type} to the ({x} {y}) benzene ring {id} site, with the heteroatom at the {qudai_idx} position'
        return msg



    def save_txt(self,name='out.txt'):
        np.savetxt(name, np.c_[self.a], fmt='%d', delimiter='\t')

    def check(self):
        for x in range(self.N):
            for y in range(self.N):
                if self.a[x][y]==1:
                    p_list=[
                        (x-1,y),(x+1,y),(x,y-1),(x,y+1)
                    ]
                    for (_x,_y) in p_list:
                        assert  self.a[_x][_y]!=1,f"{_x} {_y}"
        print('check pass')
    
    def get_index(self,index):
        for i in self.ben_class_list:
            if index == i.index:
                return i
            else:
                pass
        

    
    def scan(self):
        for(x,y) in self.ben_list:
            be = self.get_index(10000*x**2 + y**2)
            if self.a[x-1 ,y-1] == 1:
                be.node[0] = 1
                be.node[1] = 1
            if self.a[x,y-2] == 1:
                be.node[1] = 1
                be.node[2] = 1
            if self.a[x+1,y-1] == 1:
                be.node[2] =1
                be.node[3] =1
            if self.a[x+1,y+1] == 1:
                be.node[3] =1
                be.node[4] =1
            if self.a[x,y+2] == 1:
                be.node[4] =1
                be.node[5] =1
            if self.a[x-1,y+1] == 1:
                be.node[5] =1
                be.node[0] =1

   

    def get_B_H(self):
        self.B_H = 0
        for(x,y) in self.ben_list:
            if self.a[x-1,y-1]==0 and self.a[x-1,y+1]==0:
                self.B_H = self.B_H + 1
            if  self.a[x-1,y+1]==0  and self.a[x,y+2]==0 :
                self.B_H = self.B_H + 1
            if  self.a[x,y+2]==0  and self.a[x+1,y+1]==0 :
                self.B_H = self.B_H + 1
            if  self.a[x+1,y+1]==0  and self.a[x+1,y-1]==0 :
                self.B_H = self.B_H + 1
            if  self.a[x+1,y-1]==0  and self.a[x,y-2]==0 :
                self.B_H = self.B_H + 1
            if  self.a[x,y-2]==0  and self.a[x-1,y-1]==0 :
                self.B_H = self.B_H + 1
        
        return self.B_H
    
    def get_H(self):
        self.H=0
        for(x,y) in self.cyclohexane_list:
            
            if self.a[x-1,y-1] + self.a[x-1,y+1]<=0 :
                self.H = self.H + 2
            if  self.a[x-1,y+1] + self.a[x,y+2] <=0 :
                self.H = self.H + 2
            if  self.a[x,y+2] + self.a[x+1,y+1]<=0 :
                self.H = self.H + 2
            if  self.a[x+1,y+1]+ self.a[x+1,y-1]<=0 :
                self.H = self.H + 2
            if  self.a[x+1,y-1] + self.a[x,y-2]<=0 :
                self.H = self.H + 2
            if  self.a[x,y-2] +  self.a[x-1,y-1]<=0 :
                self.H = self.H+ 2
        print("The hydrogen number of cyclohexane is " + str(self.H ))
        return self.H
    

    
    def get_C_num(self):
        self.double_C=0
        self.triple_C=0
        for(x,y) in self.ben_list:
            if self.a[x-1,y-1] ==1 and self.a[x-1,y+1]==1:
                self.triple_C = self.triple_C + 1
            if self.a[x-1,y-1] ==1 and self.a[x-1,y+1]==0:
                self.double_C = self.double_C + 1
            if self.a[x-1,y-1] ==0 and self.a[x-1,y+1] ==1:
                self.double_C = self.double_C + 1
            

            if self.a[x-1,y+1] ==1 and self.a[x,y+2]==1:
                self.triple_C = self.triple_C + 1
            if self.a[x-1,y+1] ==1 and self.a[x,y+2]==0:
                self.double_C = self.double_C + 1
            if self.a[x-1,y+1] ==0 and self.a[x,y+2] ==1:
                self.double_C = self.double_C + 1
            

            if self.a[x,y+2] ==1 and self.a[x+1,y+1]==1:
                self.triple_C = self.triple_C + 1
            if self.a[x,y+2] ==1 and self.a[x+1,y+1]==0:
                self.double_C = self.double_C + 1
            if self.a[x,y+2] ==0 and self.a[x+1,y+1] ==1:
                self.double_C = self.double_C + 1
            
            if self.a[x+1,y+1] ==1 and self.a[x+1,y-1]==1:
                self.triple_C = self.triple_C + 1
            if self.a[x+1,y+1] ==1 and self.a[x+1,y-1]==0:
                self.double_C = self.double_C + 1
            if self.a[x+1,y+1] ==0 and self.a[x+1,y-1] ==1:
                self.double_C = self.double_C + 1
            

            if self.a[x+1,y-1] ==1 and self.a[x,y-2]==1:
                self.triple_C = self.triple_C + 1
            if self.a[x+1,y-1] ==1 and self.a[x,y-2]==0:
                self.double_C = self.double_C + 1
            if self.a[x+1,y-1] ==0 and self.a[x,y-2] ==1:
                self.double_C = self.double_C + 1


            if self.a[x,y-2] ==1 and self.a[x-1,y-1]==1:
                self.triple_C = self.triple_C + 1
            if self.a[x,y-2] ==1 and self.a[x-1,y-1]==0:
                self.double_C = self.double_C + 1
            if self.a[x,y-2] ==0 and self.a[x-1,y-1] ==1:
                self.double_C = self.double_C + 1
            
        print("Total number of aromatic rings："+ str(len(self.ben_list)))
        print("Total 2 carbon count:" + str(self.double_C/2))
        print("Total 3 carbon count:" + str(self.triple_C/3))
        num = 6 * len(self.ben_list) - self.double_C/2  -2 * self.triple_C/3
        print("Total carbon count：" + str(num))
        return num
    
    
    def get_ben(self,index):
        for i in self.ben_class_list:
            if i.index == index:
                return i

        exit(1)

    
    
    
    def get_available_five(self):
        self.available_five_list = []
        # self.scan()
        for(x,y) in self.ben_list:
            benhuan = self.get_ben(10000*x**2 + y**2)

            print(benhuan.node)
            if benhuan.node[0]==0 and benhuan.node[1] == 0:
                self.available_five_list.append((x,y,0))
            if benhuan.node[1]==0 and benhuan.node[2] == 0:
                self.available_five_list.append((x,y,1))
            if benhuan.node[2]==0 and benhuan.node[3] == 0:
                self.available_five_list.append((x,y,2))
            if benhuan.node[3]==0 and benhuan.node[4] == 0:
                self.available_five_list.append((x,y,3))
            if benhuan.node[4]==0 and benhuan.node[5] == 0:
                self.available_five_list.append((x,y,4))
            if benhuan.node[5]==0 and benhuan.node[0] == 0:
                self.available_five_list.append((x,y,5))
        print(self.available_five_list)
    def get_available_line(self):
        # self.scan()
        for(x,y) in self.ben_list:
            benhuan = self.get_ben(10000*x**2 + y**2)
            for i in range(0,6):
                if benhuan.node[i] ==0:
                    self.available_line.append((x,y,i))

        return self.available_line

    def add_line(self,c_num):
        available_line =self.get_available_line()
        posible_num = len(available_line)
        rand_i = np.random.randint(0, posible_num)
        (x, y, index) = available_line[rand_i]

        msg=f'Add a carbon chain of length {c_num} at {x} {y} {index}'
        print(msg)
        benhuan=self.get_ben(10000*x**2 + y**2)



        benhuan.node[index]=C_Line(x,y,index,c_num)

        self.lines_list.append(benhuan.node[index])

        return msg
    def add_pyridine(self):
        available_line = self.get_available_line()
        posible_num = len(available_line)
        rand_i = np.random.randint(0, posible_num)
        (x, y, index) = available_line[rand_i]

        rand_j = np.random.randint(0, 5)

        msg=f'Binding the {rand_j} locus of pyridine at {x} {y} {index}'
        print(msg)
        benhuan = self.get_ben(10000 * x ** 2 + y ** 2)
        from class_pyridine import Pyridine

        pyridine_idx = np.random.randint(0, 5)
        benhuan.node[index] = Pyridine(x, y, index, pyridine_idx)

        return msg
    def add_yafeng(self):
        posible_num = len(self.lines_list)
        rand_i = np.random.randint(0, posible_num)

        line_shili=self.lines_list.pop(rand_i)
        rand_j=np.random.randint(0,line_shili.c_num-1)



        msg=f"Add sulfoxide to the {line_shili.x} {line_shili.y} of the benzene ring of the {line_shili.start_idx} side chain {rand_j} after the carbon"
        print(msg)
        return msg

    def print_structure(self):
        self.check()
        x_min=self.N
        x_max=-1
        y_min=self.N
        y_max=-1
        for (x,y) in self.ben_list:
            x_min=min(x_min,x)
            x_max=max(x_max,x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)

        for (x,y) in self.cyclohexane_list:
            x_min=min(x_min,x)
            x_max=max(x_max,x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
        # print(x_min, x_max)
        # print(y_min,y_max)

        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                if self.a[x][y]==1:
                    ring_type='benzene'
                    # print('b',end='')
                    figure_x= self.g.center_x+(y-self.center_y)*self.g.gap
                    figure_y= self.g.center_y+(x-self.center_x)*self.g.a*3/2
                    # print(self.g.center_x+(x-self.center_x)*self.g.gap,y-self.center_y)
                    # print(x,y)
                    # print(figure_x,figure_y)
                    
                    self.g.add_6ring(figure_x,figure_y,ring_type)
                elif self.a[x][y]==2:
                    ring_type='cyclohexane'
                    # print('c',end='')
                    figure_x= self.g.center_x+(y-self.center_y)*self.g.gap
                    figure_y= self.g.center_y+(x-self.center_x)*self.g.a*3/2
                    # print(self.g.center_x+(x-self.center_x)*self.g.gap,y-self.center_y)
                    # print(x,y)
                    # print(figure_x,figure_y)

                    self.g.add_6ring(figure_x,figure_y,ring_type)
                else:
                    # print(' ', end='')
                    pass
            # print('')
        for (x,y,c_id,qudai_idx,ring_type) in self.ring5_list:
            # print('---')
            self.g.add_5ring(x,y,self.center_x,self.center_y,c_id,qudai_idx,'呋喃')
        self.g.generate()







