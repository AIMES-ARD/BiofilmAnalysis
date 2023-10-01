import numpy
import pandas
from aicsimageio import AICSImage

info = {}
info["xlsxname"] = "IntensityPerSlice.xlsx"

info["path_OX"] =  "./OX/"
info["files_OX"] = ("Experiment-96.czi - Experiment-96.czi #4.tif", "Experiment-109.czi - Experiment-109.czi #1.tif", "slide2Experiment-198.czi - slide2Experiment-198.czi #1.tif")

info["path_RED"] = "./RED/"
info["files_RED"] = ("Experiment-96.czi - Experiment-96.czi #1.tif", "Experiment-112.czi - Experiment-112.czi #4.tif", "slide3Experiment-197.czi - slide3Experiment-197.czi #1.tif")


conditions = ("OX", "RED")
colors = ("Ebba", "GFP")

with pandas.ExcelWriter(info["xlsxname"]) as writer:

    for condition in conditions:
        data = {}
        for f, file in enumerate(info["files" + "_" + condition]):
            print(file)

            img = AICSImage(info["path" + "_" + condition] + file)
            RED =  img.get_image_data("ZYX", C=0, S=0, T=0)
            GREEN =  img.get_image_data("ZYX", C=1, S=0, T=0)

            intensityperslice_red = []
            intensityperslice_green = []
            for s in range(numpy.shape(GREEN)[0]):
                intensityperslice_red.append(RED[s,:,:].sum())
                intensityperslice_green.append(GREEN[s,:,:].sum())

            
            max_red = numpy.argmax(intensityperslice_red)
            max_green = numpy.argmax(intensityperslice_green)

            col_red = numpy.zeros((60)) 
            col_green = numpy.zeros((60)) 

            col_red[:] = numpy.nan
            col_green[:] = numpy.nan

            diff_red = 30-max_red
            diff_green = 30-max_green

            # print(diff_green, diff_red)
            col_red[diff_red:len(intensityperslice_red)+diff_red] = intensityperslice_red
            col_green[diff_green:len(intensityperslice_green)+diff_green] = intensityperslice_green


            data[condition + "_" + "Ebba" + "_" + str(f)] = col_red
            data[condition + "_" + "GFP" + "_" + str(f)] = col_green

        df_out = pandas.DataFrame(data)
        df_out.to_excel(writer, sheet_name=condition)


