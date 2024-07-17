import numpy
import pandas
from aicsimageio import AICSImage

czi = "./DATA/SH1000_airy_Ebba680+.czi"
xlsx = "test.xlsx"
img = AICSImage(czi)
RED =  img.get_image_data("ZYX", C=0, S=0, T=0)
GREEN =  img.get_image_data("ZYX", C=1, S=0, T=0)

data = {}

intensityperslice_red = []
intensityperslice_green = []
for s in range(numpy.shape(GREEN)[0]):
    intensityperslice_red.append(RED[s,:,:].sum())
    intensityperslice_green.append(GREEN[s,:,:].sum())

data["Ebba"] = intensityperslice_red
data["GFP"] = intensityperslice_green

with pandas.ExcelWriter(xlsx) as writer:

    df_out = pandas.DataFrame(data)
    df_out.to_excel(writer)


