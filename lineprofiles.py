import numpy
import pandas
from aicsimageio import AICSImage

info = {}
info["xlsxname"] = "LineProfiles.xlsx"

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

            sum_red = numpy.sum(RED, axis=0)
            sum_green = numpy.sum(GREEN, axis=0)
            
            # print(numpy.shape(sum_red), numpy.shape(sum_green))
            average_red = numpy.average(sum_red, axis=1) / 1e4
            average_green = numpy.average(sum_green, axis=1) / 1e4

            max_red = numpy.argmax(average_red)
            max_green = numpy.argmax(average_green)

            col_red = numpy.zeros((6000)) 
            col_green = numpy.zeros((6000)) 

            col_red[:] = numpy.nan
            col_green[:] = numpy.nan

            diff_red = 2400-max_red
            diff_green = 2400-max_green

            # print(diff_green, diff_red)
            col_red[diff_red:len(average_red)+diff_red] = average_red
            col_green[diff_green:len(average_green)+diff_green] = average_green

            # print(numpy.shape(average_red), numpy.shape(average_green))
            data[condition + "_" + "Ebba" + "_" + str(f)] = col_red    
            data[condition + "_" + "GFP" + "_" + str(f)] = col_green
            
        df_out = pandas.DataFrame(data)
        df_out.to_excel(writer, sheet_name=condition)
