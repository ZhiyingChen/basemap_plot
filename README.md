# basemap_plot
**Introduction**

突然找到自己大二时候画的中国植被分布图代码，所以整理了一下代码做记录。

**Datasets**

这是一个用Basemap库绘制分布的工程，部分相关数据放进了Datasets文件夹，来源如下。

		数据集1:Land cover 植被数据
		Source: https://glad.umd.edu/dataset/long-term-global-land-change  
		Details: 每年基于卫星探测的植被数据，其中涵盖了1982 - 2016年的三种不同类型（TC，SV，BG）

		数据集2:ERA-Interim 云量
		Source:https://www.ecmwf.int/en/forecasts/datasets    
		Details: 1982 - 2016年LCC和TCC等因素的月平均数据
		
		数据集3:中国地图数据
		Source:http://www.diva-gis.org/datadown

**Plot**

效果还挺好看的

中国2016年TreeCover分布图

![image](https://raw.githubusercontent.com/ZhiyingChen/basemap_plot/main/images/Distribution%20of%20TC%20in%202016.png)


中国秦岭地区1983和2016年低矮云层四季分布对比图

<img src="https://raw.githubusercontent.com/ZhiyingChen/basemap_plot/main/images/QL%20Distribution%20of%20LCC.png" style="width:700px; height:700px">

**Environment Deployment**

Install Python Executor (version >= 3.9.0), Anaconda IDE is recommanded

The required packages are listed in requirements.txt. you can install them using:

    pip install -r requirements.txt
	

**Run**

To run project:

	1. Set the working directory as the root folder.
    2. execute python main.py
	
