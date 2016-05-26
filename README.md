# 3DModelSegmentation
#### 本项目是利用前段时间爬取的Collada三维建筑模型作为实验数据,基于Kmeans++聚类算法来对模型进行分割,分割成有意义的五部分.

#### 环境
+ 系统:ubuntu14.04 64位
+ jdk:1.7

#### 安装相关包
安装Collada之前需要先安装一些依赖
+ sudo apt-get install python-lxml python-numpy python-dateutil
+ easy_install pycollada

安装vtk,用于显示模型
+ sudo apt-get install python-vtk

安装matplotlib,用于画点云图
+ sudo apt-get install python-matplotlib

#### 启动
+ cd 3DModelSegmentation
+ python segmentation.py

#### 还需注意的是,三维模型的导入路径需要根据自己的路径做相应改变.我在model文件夹下放置了一个Collada模型,以供实验.
