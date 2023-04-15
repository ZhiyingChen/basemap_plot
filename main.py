from src.plant_dist import VegName, PlantDist
from src.cloud_dist import CloudName, SeasonName, CloudDist
import src.config as cf


if __name__ == "__main__":
    # 绘制中国植被分布
    filepath = cf.PLANT_FILE_PATH
    filename = filepath + cf.PLANT_FILE_2016

    ChinaPlant = PlantDist(filename, output_folder=cf.PLOT_OUTPUT)
    ChinaPlant.generate_data()
    ChinaPlant.drawPic(dataName=VegName.TC, title='Distribution of TreeCover of China in 2016')
    ChinaPlant.drawPic(dataName=VegName.NTV, title='Distribution of NonTree Vegetation of China in 2016')
    ChinaPlant.drawPic(dataName=VegName.NV, title='Distribution of NonVegetated of China in 2016')

    # 绘制中国秦岭地区的云量分布
    filepath = cf.COULD_FILE_PATH
    filename = filepath + cf.CLOUD_FILE_2016

    # 绘制春夏秋冬的Low Cloud Cover
    ChinaQLCloud = CloudDist(filename, output_folder=cf.PLOT_OUTPUT)
    ChinaQLCloud.generate_data()
    ChinaQLCloud.drawSeasonPic(dataName=CloudName.LCC, season=SeasonName.Spring,
                               title='Distribution of Low Could Cover of Spring in 2016')