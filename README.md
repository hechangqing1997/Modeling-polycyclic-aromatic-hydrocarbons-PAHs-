# Molecular-Reconstruction

## 目录
* [文件目录](#文件目录)

```
codevv4
└─ codev4
   ├─ .DS_Store
   ├─ .idea(基本信息)
   │  ├─ codev4.iml
   │  ├─ deployment.xml
   │  ├─ inspectionProfiles
   │  │  └─ profiles_settings.xml
   │  ├─ misc.xml
   │  ├─ modules.xml
   │  └─ workspace.xml
   ├─ ann.py(神经网络)
   ├─ benzene.py(苯环类)
   ├─ build.py(搭建配置文件)
   ├─ class_ben.py(苯环类)
   ├─ class_pyridine.py(吡啶类)
   ├─ config(配置文件)
   │  ├─ example.yml
   │  ├─ example1.yml
   │  ├─ iaa.yml
   │  ├─ __init__.py
   │  └─ __pycache__
   │     ├─ __init__.cpython-38.pyc
   │     └─ __init__.cpython-39.pyc
   ├─ cyclohexane.py(环己烷类)
   ├─ data(运行完get_data.py以后，生成的data放在这里)
   ├─ get_data.py(用于生成训练的data)
   ├─ iaa.py(神经网络类)
   ├─ img_plot(超参数实验生成的图像以及存储loss数据的txt文件)
   │  ├─ 1e-09.txt
   │  ├─ 1e-10.txt
   │  ├─ 1e-11.txt
   │  ├─ 5e-10.txt
   │  ├─ 5e-11.txt
   │  ├─ e-10.txt
   │  ├─ loss-e-10.png
   │  └─ loss.png
   ├─ line.py(脂肪链类)
   ├─ log.txt(记录log信息,用于判断最后的拼接位点)
   ├─ logger.py(logger类,用于生成log)
   ├─ main_SR.py(随机生成分子类,用于随机生成分子模型并求解出各种参数)
   ├─ mytrain.py(用于训练神经网络)
   ├─ optimizer.py(用于计算各种loss)
   ├─ out.txt(用于存储最后的矩阵文件)
   ├─ output(用于存储生成的模型,可以用浏览器打开)
   ├─ README.md
   ├─ ring5.py(5元环类)
   ├─ sample.py(SR过程的主要代码)
   ├─ svg_parser_master(用于画图)
   │  ├─ benzene-ring-155277.svg
   │  ├─ benzene.svg
   │  ├─ example.svg
   │  ├─ generate_svg.py
   │  ├─ svg_parser.py
   │  ├─ tmp.svg
   │  └─ __pycache__
   │     ├─ generate_svg.cpython-38.pyc
   │     ├─ generate_svg.cpython-39.pyc
   │     └─ svg_parser.cpython-38.pyc
   ├─ train.py(用于训练神经网络,传进去所有参数)
   ├─ train_clear.py(用于训练神经网络,alpha与gama氢的参数没有传)
   └─ __pycache__(缓存文件，不用管)
      ├─ benzene.cpython-38.pyc
      ├─ benzene.cpython-39.pyc
      ├─ class_ben.cpython-38.pyc
      ├─ class_ben.cpython-39.pyc
      ├─ class_pyridine.cpython-39.pyc
      ├─ cyclohexane.cpython-38.pyc
      ├─ cyclohexane.cpython-39.pyc
      ├─ line.cpython-38.pyc
      ├─ line.cpython-39.pyc
      ├─ main_SR.cpython-39.pyc
      ├─ ring5.cpython-38.pyc
      ├─ ring5.cpython-39.pyc
      ├─ sample.cpython-38.pyc
      └─ sample.cpython-39.pyc

```
    
* [运行方法](#运行方法)

```
python get_data.py  
用于生成训练数据
 
python train.py  或者 python train_clear.py
用于训练神经网络

python main_SR.py 
用于生成模型(默认生成100个最好的模型)
```

