import src.config as cf
import os
from netCDF4 import Dataset
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#定义了两个函数，将经纬度转化成所在的格点位置
def lon2index(lon):
    index=(lon)/0.75
    return int(index)

def lat2index(lat):
    index=-((lat-90.)/0.75)
    return int(index)

class CloudName:
    TCC = 'Total Cloud Cover'
    LCC = 'Low Cloud Cover'

class SeasonName:
    Spring = 'spring'
    Summer = 'summer'
    Autumn = 'autumn'
    Winter = 'winter'

class CloudDist:
    def __init__(self, filename, output_folder):
        self.filename = filename
        self.output_folder = output_folder
        self.filepath_map = cf.CHINA_MAP_FILE
        # 输入经纬度：读取中国秦岭地区的数据
        self.lonstart = lon2index(cf.CHINA_QL_DATA['lonstart'])
        self.lonend = lon2index(cf.CHINA_QL_DATA['lonend'])
        self.latend = lat2index(cf.CHINA_QL_DATA['latend'])
        self.latstart = lat2index(cf.CHINA_QL_DATA['latstart'])
        self.longtitude = None
        self.latitude = None
        self.TCC = None
        self.LCC = None
        self.CloudDict = dict()
        self.seasonDict = {
            SeasonName.Spring: [2, 3, 4],
            SeasonName.Summer: [5, 6, 7],
            SeasonName.Autumn: [8, 9, 10],
            SeasonName.Winter: [0, 1, 11]
        }

    def getCloudData(self):
        filename_cloud = self.filename
        lonstart_cloud = self.lonstart
        lonend_cloud = self.lonend
        latend_cloud = self.latend
        latstart_cloud = self.latstart

        ncobj_cloud = Dataset(filename_cloud)
        lon_cloud = ncobj_cloud.variables['longitude'][:]
        lat_cloud = ncobj_cloud.variables['latitude'][:]

        self.longtitude = lon_cloud[lonstart_cloud: lonend_cloud + 1]
        self.latitude = lat_cloud[latstart_cloud: latend_cloud + 1]

    def getCloudDis(self):
        filename = self.filename
        lonstart = self.lonstart
        lonend = self.lonend
        latend = self.latend
        latstart = self.latstart

        ncobj_cloud = Dataset(filename)
        # 将秦岭地区的数据存入列表中 注意存储数据都是int型变量 后面要是要合并 就都要改成float类型
        current_lcc = ncobj_cloud.variables['lcc'][:]
        current_tcc = ncobj_cloud.variables['tcc'][:]
        lcc = np.array(current_lcc[:, latstart:latend + 1, lonstart:lonend + 1], dtype=float)
        tcc = np.array(current_tcc[:, latstart:latend + 1, lonstart:lonend + 1], dtype=float)

        self.TCC = tcc
        self.LCC = lcc

        self.CloudDict = {
            CloudName.TCC: self.TCC,
            CloudName.LCC: self.LCC
        }

    def mkOutput(self):
        try:
            os.mkdir(self.output_folder)
        except:
            pass

    def generate_data(self):
        self.getCloudData()
        self.getCloudDis()
        self.mkOutput()

    def drawMonthPic(self, dataName, month, title):
        """
        开始绘制 season 的 TCC / LCC
        """

        filepath_map = self.filepath_map
        longtitude, latitude = self.longtitude, self.latitude

        map = Basemap(llcrnrlon=105.75,
                               llcrnrlat=30.,
                               urcrnrlon=111.,
                               urcrnrlat=32.25,
                               projection='cass', lat_0=31., lon_0=107.5)

        map.readshapefile(filepath_map, 'states', drawbounds=True)

        map.drawcoastlines()

        parallels = np.arange(29., 33., 1.)
        map.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)  # 绘制纬线

        meridians = np.arange(105., 112., 2.)
        map.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)  # 绘制经线

        m, n = np.meshgrid(np.array(longtitude), np.array(latitude))
        a, b = map(m, n)
        lvls = np.arange(0, 0.5, 0.05)

        CC = self.CloudDict[dataName][month, :, :]
        fig = map.contourf(a, b, CC[-1], alpha=0.5, cmap='spring', levels=lvls)
        # The alpha blending value, between 0 (transparent) and 1 (opaque).
        bar = map.colorbar(fig, 'right', ticks=np.arange(0, 0.6, 0.1), format='%.1f')

        font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 16}
        plt.title(title, font1)
        # plt.show()
        plt.savefig(self.output_folder + title + '.png')

    def drawSeasonPic(self, dataName, season, title):
        """
        开始绘制 season 的 TCC / LCC
        """

        filepath_map = self.filepath_map
        longtitude, latitude = self.longtitude, self.latitude

        map = Basemap(llcrnrlon=105.75,
                      llcrnrlat=30.,
                      urcrnrlon=111.,
                      urcrnrlat=32.25,
                      projection='cass', lat_0=31., lon_0=107.5)

        map.readshapefile(filepath_map, 'states', drawbounds=True)

        map.drawcoastlines()

        parallels = np.arange(29., 33., 1.)
        map.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)  # 绘制纬线

        meridians = np.arange(105., 112., 2.)
        map.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)  # 绘制经线

        m, n = np.meshgrid(np.array(longtitude), np.array(latitude))
        a, b = map(m, n)
        lvls = np.arange(0, 0.5, 0.05)

        month_lt = self.seasonDict[season]
        CC = (self.CloudDict[dataName][month_lt[0], :, :] +
              self.CloudDict[dataName][month_lt[1], :, :] +
              self.CloudDict[dataName][month_lt[2], :, :]) / 3.
        fig = map.contourf(a, b, CC, alpha=0.5, cmap=season, levels=lvls)
        # The alpha blending value, between 0 (transparent) and 1 (opaque).
        bar = map.colorbar(fig, 'right', ticks=np.arange(0, 0.6, 0.1), format='%.1f')

        font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 16}
        plt.title(title, font1)
        # plt.show()
        plt.savefig(self.output_folder + title + '.png')



if __name__ == "__main__":

    # 绘制中国秦岭地区的云量分布
    filepath = cf.COULD_FILE_PATH
    filename = filepath + cf.CLOUD_FILE_2016

    # 绘制春夏秋冬的Total Cloud Cover
    ChinaQLCloud = CloudDist(filename, output_folder=cf.PLOT_OUTPUT)
    ChinaQLCloud.generate_data()
    ChinaQLCloud.drawSeasonPic(dataName=CloudName.TCC, season=SeasonName.Spring,
                               title='Distribution of Total Could Cover of Spring in 2016')