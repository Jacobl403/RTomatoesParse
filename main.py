import time
import data_parser as dp
from preprocessdata import PreprocessData
from util import CsvFileHelper


# Download latest version
def init():
    CsvFileHelper.wipe_out_dir()
    test = dp.DataParser()
    start = time.time()
    test.run()
    end = time.time()
    print("done saving data to test.csv. Executed in {} ... \n".format(float(end - start)))


if __name__ == '__main__':
    # init()
    PreprocessData().preprocess()







# URI = "https://www.rottentomatoes.com/m/madame_web"
#
# reviewsAttr = "/reviews"
#
# topCriticsAttr = "/reviews?type=top_critics"
#
# allAudienceAttr = "/reviews?type=user"
#
# verifiedAudience = "/reviews?type=verified_audience"
