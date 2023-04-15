import src.config as cf
import os
from netCDF4 import Dataset
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


# 定义了两个函数，将经纬度转化成所在的格点位置
def lon2index(lon):
    index = (lon + 180) / 0.05
    return int(index)


def lat2index(lat):
    index = -((lat - 90) / 0.05)
    return int(index)

class VegName:
    TC = 'TreeCover'
    NTV = 'NonTree_Vegetation'
    NV = 'NonVegetated'

class PlantDist:
    def __init__(self, filename, output_folder):
        self.filename = filename
        self.output_folder = output_folder
        self.filepath_map = cf.CHINA_MAP_FILE
        # 输入经纬度：读取中国的数据
        self.lonstart = lon2index(cf.CHINA_DATA['lonstart'])
        self.lonend = lon2index(cf.CHINA_DATA['lonend'])
        self.latend = lat2index(cf.CHINA_DATA['latend'])
        self.latstart = lat2index(cf.CHINA_DATA['latstart'])
        self.longtitude = None
        self.latitude = None
        self.TC = None
        self.NTV = None
        self.NV = None
        self.VegDict = dict()

    def getVegData(self):
        filename = self.filename
        lonstart = self.lonstart
        lonend = self.lonend
        latend = self.latend
        latstart = self.latstart

        ncobj = Dataset(filename)
        lon = ncobj.variables['lon'][:]
        lat = ncobj.variables['lat'][:]

        longtitude = lon[lonstart:lonend]
        latitude = lat[latstart:latend]

        self.longtitude = longtitude
        self.latitude = latitude

    def getVegDis(self):
        filename = self.filename
        lonstart = self.lonstart
        lonend = self.lonend
        latend = self.latend
        latstart = self.latstart

        ncobj = Dataset(filename)

        # 将中国的数据存入列表中 注意存储数据都是int型变量 后面要是要合并 就都要改成float类型
        current_TreeCover = ncobj.variables[VegName.TC][:]
        current_NonTree_Vegetation = ncobj.variables[VegName.NTV][:]
        current_NonVegetated = ncobj.variables[VegName.NV][:]
        TC = np.array(current_TreeCover[0][latstart:latend, lonstart:lonend], dtype=float)
        NTV = np.array(current_NonTree_Vegetation[0][latstart:latend, lonstart:lonend], dtype=float)
        NV = np.array(current_NonVegetated[0][latstart:latend, lonstart:lonend], dtype=float)

        self.TC = TC
        self.NTV = NTV
        self.NV = NV
        self.VegDict = {
            VegName.TC: self.TC,
            VegName.NTV: self.NTV,
            VegName.NV: self.NV
        }

    def mkOutput(self):
        try:
            os.mkdir(self.output_folder)
        except:
            pass

    def generate_data(self):
        self.getVegData()
        self.getVegDis()
        self.mkOutput()

    def drawPic(self, dataName, title):
        """
           开始绘制 InputData: TreeCover/ Non Tree Vegetation / NonVegetated
        """

        filepath_map = self.filepath_map
        longtitude, latitude = self.longtitude, self.latitude

        map = Basemap(llcrnrlon=80.33,
                        llcrnrlat=3.01,
                        urcrnrlon=138.16,
                        urcrnrlat=56.123,
                        resolution='h', projection='cass', lat_0=42.5, lon_0=120)

        map.readshapefile(filepath_map, 'states', drawbounds=True)

        # map.shadedrelief() # 绘制阴暗的浮雕图

        # map.etopo() # 绘制地形图，浮雕样式

        map.drawcoastlines()

        parallels = np.arange(0., 90, 10.)
        map.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)  # 绘制纬线

        meridians = np.arange(80., 140., 10.)
        map.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)  # 绘制经线

        x, y = map(116.405289, 39.904987)  # 北京市坐标，经纬度坐标转换为该map的坐标
        map.scatter(x, y, s=200, marker='*', facecolors='r', edgecolors='r')  # 绘制首都

        m, n = np.meshgrid(longtitude, latitude)
        a, b = map(m, n)
        lvls = np.arange(0, 100, 10)

        InputData = self.VegDict[dataName]
        fig = map.contourf(a, b, InputData, alpha=0.5, cmap='Greens', levels=lvls)
        # The alpha blending value, between 0 (transparent) and 1 (opaque).
        bar = map.colorbar(fig, 'right', ticks=np.arange(0, 100, 20), format='%.1f')

        font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 16}
        plt.title(title, font1)
        # plt.show()
        plt.savefig(self.output_folder + title + '.png')



