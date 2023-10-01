import numpy
import pandas
from aicsimageio import AICSImage
from scipy.stats import entropy

info = {}
info["xlsxname"] = "Histograms.xlsx"

info["path_OX"] =  "./OX/"
info["files_OX"] = ("Experiment-96.czi - Experiment-96.czi #4.tif", "Experiment-109.czi - Experiment-109.czi #1.tif", "slide2Experiment-198.czi - slide2Experiment-198.czi #1.tif")

info["path_RED"] = "./RED/"
info["files_RED"] = ("Experiment-96.czi - Experiment-96.czi #1.tif", "Experiment-112.czi - Experiment-112.czi #4.tif", "slide3Experiment-197.czi - slide3Experiment-197.czi #1.tif")


conditions = ("OX", "RED")
colors = ("Ebba", "GFP")

nbins = 256
binrange = (0, 65280)

with pandas.ExcelWriter(info["xlsxname"]) as writer:

    entropydata = {}
    for condition in conditions:
            
        data = {} 
        data2 = {}
        for f, file in enumerate(info["files" + "_" + condition]):
            print(file)

            img = AICSImage(info["path" + "_" + condition] + file)
            RED =  img.get_image_data("ZYX", C=0, S=0, T=0)
            GREEN =  img.get_image_data("ZYX", C=1, S=0, T=0)

            sum_red = numpy.sum(RED, axis=0)
            sum_green = numpy.sum(GREEN, axis=0)           

            hist_red, bins = numpy.histogram(sum_red, bins=nbins, range=binrange)
            hist_green, bins = numpy.histogram(sum_green, bins=nbins, range=binrange)
            
            max_red = numpy.argmax(hist_red)
            max_green = numpy.argmax(hist_green)

            col_red = numpy.zeros((500)) 
            col_green = numpy.zeros((500)) 

            col_red[:] = numpy.nan
            col_green[:] = numpy.nan

            diff_red = 20-max_red
            diff_green = 20-max_green

            # print(diff_green, diff_red)
            col_red[diff_red:len(hist_red)+diff_red] = hist_red
            col_green[diff_green:len(hist_green)+diff_green] = hist_green
            
            data[condition + "_" + "Ebba" + "_" + str(f)] = hist_red  
            data[condition + "_" + "GFP" + "_" + str(f)] = hist_green

            data[condition + "_" + "Ebba" + "_" + str(f)] = col_red  
            data[condition + "_" + "GFP" + "_" + str(f)] = col_green

            probdist_red = hist_red / hist_red.sum()
            probdist_green = hist_green / hist_green.sum()
            imageentropy_red = entropy(probdist_red, base=2)
            imageentropy_green = entropy(probdist_green, base=2)

            entropydata[condition + "_"+ "Ebba" + "_" + str(f)] = imageentropy_red
            entropydata[condition + "_"+ "GFP" + "_" + str(f)] = imageentropy_green
        
        df_out = pandas.DataFrame(data)
        df_out2 = pandas.DataFrame(entropydata, index=[0])
        df_out.to_excel(writer, sheet_name=condition)
        df_out2.to_excel(writer, sheet_name="entropy")

