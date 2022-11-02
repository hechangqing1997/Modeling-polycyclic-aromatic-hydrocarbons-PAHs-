
from lib2to3.pytree import HUGE
import numpy as np
np.random.seed(2)
from xml.dom.minidom import parse
import xml.dom.minidom
import math
class Generate_svg():
    def __init__(self,length_x=3000,length_y=3000,a=100,file_name='tmp.svg') -> None:
        self.length_x=length_x
        self.length_y=length_y
        self.center_x=self.length_x/2
        self.center_y=self.length_y/2
        self.a=a
        self.gap=pow(3,0.5)*self.a/2
        self.file_name=file_name
        self.ring6_list=[]
        self.ring5_list=[]
        self.init_svg()
        
    def init_svg(self):
        self.svg_start=f"""<?xml version="1.0" encoding="UTF-8"?>
<svg version="1.1" viewBox="0 0 {self.length_x} {self.length_y}" xmlns="http://www.w3.org/2000/svg">
"""
        self.svg_end="""</svg>
"""

        with open(self.file_name,'w') as f:
            f.write(self.svg_start+self.svg_end)
        
    def add_6ring(self,x,y,ring_type):
        
        a=self.a
        deltax=self.a/2*pow(3,0.5)
        points=[
            (x,y-a),(x-deltax,y-a/2),(x,y+a),(x+deltax,y+a/2)
        ]
        if ring_type=='benzene':
            temp=f"""<g fill="none" stroke="#000">
                <path d="M{points[0][0]} {points[0][1]} L {points[1][0]} {points[1][1]} v {a} L {points[2][0]} {points[2][1]} L {points[3][0]} {points[3][1]} v -{a} L {points[0][0]} {points[0][1]} "/>
                <circle cx="{x}" cy="{y}" r='{0.7*a}' stroke='black' fill="none" stroke-width="1"/>
    </g>
    """ 
        elif ring_type=='cyclohexane':
             temp=f"""<g fill="none" stroke="#000">
                <path d="M{points[0][0]} {points[0][1]} L {points[1][0]} {points[1][1]} v {a} L {points[2][0]} {points[2][1]} L {points[3][0]} {points[3][1]} v -{a} L {points[0][0]} {points[0][1]} "/>
    </g>
    """ 
        self.ring6_list.append(temp)
        return temp
    
    def add_5ring(self,x_index_matrix,y_index_matrix,x_center_matrix,y_center_matrix,c_id,qudai_idx,ring_type):
        
        
        a=self.a
        b=(a/2)/math.sin(math.radians(36))
        
        hudgree=math.radians(60)
        # print(hudgree)
        l=math.sin(hudgree)*a+a/2*math.tan(math.radians(54))
        # print(l)
        figure_x=self.center_x+(y_index_matrix-y_center_matrix)*self.gap
        figure_y=self.center_y+(x_index_matrix-x_center_matrix)*a*3/2
        
        degree=-1
        if c_id==0:
            degree=30
           
        elif c_id==1:
            degree=90
        elif c_id==2:
            degree=150
        elif c_id==3:
            degree=210
        elif c_id==4:
            degree=270
        elif c_id==5:
            degree=330
        rot_d=degree+90
        ring_x=figure_x+l*math.cos(math.radians(rot_d))
        ring_y=figure_y-l*math.sin(math.radians(rot_d))
        
        # print(ring_x,ring_y)
        temp=self.draw_5ring(ring_x,ring_y,figure_x,figure_y,b,degree)
        self.ring5_list.append(temp)
        return temp

    def draw_5ring(self,ring_x,ring_y,s_x,s_y,b,degree):
        
        
        # degree=30
        p_list=[]
    
        p_list.append((0,-b))
        p_list.append((b*math.cos(math.radians(162)),-b*math.sin(math.radians(162))))
        p_list.append((b*math.cos(math.radians(234)),-b*math.sin(math.radians(234))))
        p_list.append((b*math.cos(math.radians(306)),-b*math.sin(math.radians(306))))
        p_list.append((b*math.cos(math.radians(18)),-b*math.sin(math.radians(18))))
        points=[]
        for (deltax,deltay) in p_list:
            points.append((ring_x+deltax,ring_y+deltay))
        temp=f"""<g fill="none" stroke="#000" transform='rotate(-{degree} {ring_x} {ring_y})'>
                <path d="M{points[0][0]} {points[0][1]} L {points[1][0]} {points[1][1]}  L {points[2][0]} {points[2][1]} L {points[3][0]} {points[3][1]}  L {points[4][0]} {points[4][1]} L {points[0][0]} {points[0][1]}"/>
    </g>
    """ 
        return temp
    def generate_demo(self):
        
        self.add_6ring(self.center_x,self.center_y,'苯环')
        self.add_5ring(15,15,15,15,5,1,'呋喃')
        self.generate()
       
    def ring5_demo(self):
        figure_x=1500
        figure_y=1500
        degree=270
        p_list=[]
        a=self.a
        b=(a/2)/math.sin(math.radians(36))
        
        p_list.append((0,-b))
        p_list.append((b*math.cos(math.radians(162)),-b*math.sin(math.radians(162))))
        p_list.append((b*math.cos(math.radians(234)),-b*math.sin(math.radians(234))))
        p_list.append((b*math.cos(math.radians(306)),-b*math.sin(math.radians(306))))
        p_list.append((b*math.cos(math.radians(18)),-b*math.sin(math.radians(18))))
        
        points=[]
        for (deltax,deltay) in p_list:
            points.append((figure_x+deltax,figure_y+deltay))
        temp=f"""<g fill="none" stroke="#000" transform='rotate(-{degree} {points[2][0]} {points[2][1]})'>
                <path d="M{points[0][0]} {points[0][1]} L {points[1][0]} {points[1][1]}  L {points[2][0]} {points[2][1]} L {points[3][0]} {points[3][1]}  L {points[4][0]} {points[4][1]} L {points[0][0]} {points[0][1]}"/>
    </g>
    """ 
        self.ring5_list.append(temp)
        self.generate()
    def generate(self):
        svg_list=[]
        svg_list.append(self.svg_start)
        svg_list.extend(self.ring6_list)
        svg_list.extend(self.ring5_list)
        svg_list.append(self.svg_end)
        # print(len(svg_list))
        svg=''
        for snip in svg_list:
            svg=svg+snip
            
        with open(self.file_name,'w') as f:
            f.write(svg)
def parser_svg():
    
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("benzene.svg")
    collection = DOMTree.documentElement

if __name__=="__main__":
    g=Generate_svg()
    g.generate_demo()
    