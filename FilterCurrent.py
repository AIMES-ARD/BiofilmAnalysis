import pandas
from scipy.signal import savgol_filter

info = {}

info["filename_in"] = "CURRENTDATA.xlsx"
info["filename_out"] = "FILTEREDCURRENTS.xlsx"

info["sheetname_ARD204_OX"] = "ARD204 OX" 
info["colums_ARD204_OX"] =  ("[muA] EXP-22-DR4263", "[muA] EXP-22-DR4264", "[muA] EXP-22-DR4265", "[muA] EXP-23-DR4296", "[muA] EXP-23-DR4297", "[muA] EXP-23-EA0801")
info["param_ARD204_OX"] = 50

info["sheetname_ARD204_RED"] = "ARD204 RED" 
info["colums_ARD204_RED"] =  ("[muA] EXP-22-DR4263", "[muA] EXP-22-DR4264", "[muA] EXP-22-DR4265", "[muA] EXP-23-DR4296", "[muA] EXP-23-DR4297", "[muA] EXP-23-EA0801")
info["param_ARD204_RED"] = 50

info["sheetname_ARD204_0V"] = "ARD204 0V" 
info["colums_ARD204_0V"] = ("[muA] EXP-23-DR4287 CHA", "[muA] EXP-23-DR4287 CHB",	"[muA] EXP-23-DR4290 CHA", "[muA] EXP-23-DR4290 CHB", "[muA] EXP-22-DR4253")
info["param_ARD204_0V"] = 50

info["sheetname_LB_OX"] = "LB OX" 
info["colums_LB_OX"] = ("[muA] EXP-22-DR4256 1", "[muA]  EXP-22-DR4256 2", "[muA] EXP-23-EA0810")
info["param_LB_OX"] = 50

info["sheetname_LB_RED"] = "LB RED" 
info["colums_LB_RED"] = ("[muA] EXP-22-DR4255", "[muA] EXP-23-EA0810")
info["param_LB_RED"] = 50

info["sheetname_LB_0V"] = "LB 0V" 
info["colums_LB_0V"] = ("[muA] EXP-23-EA0810 CHA", "[muA] EXP-23-EA0810 CHB")
info["param_LB_0V"] = 50

info["sheetname_ARD206_OX"] = "ARD206 OX" 
info["colums_ARD206_OX"] = ("[muA] EXP-23-DR4289",	"[muA] EXP-23-DR4291", "[muA] EXP-23-DR4294", "[muA] EXP-23-EA0801")
info["param_ARD206_OX"] = 50

info["sheetname_ARD206_RED"] = "ARD206 RED" 
info["colums_ARD206_RED"] = ("[muA] EXP-23-DR4289", "[muA] EXP-23-DR4291", "[muA] EXP-23-DR4293", "[muA] EXP-23-DR4294", "[muA] EXP-23-EA0801")
info["param_ARD206_RED"] = 50

info["sheetname_ARD207_OX"] = "ARD207 OX" 
info["colums_ARD207_OX"] = ("[muA] EXP-22-DR4259", "[muA] EXP-23-DR4288", "[muA] EXP-23-DR4299", "[muA] EXP-23-EA0800", "[muA] EXP-23-EA0802")
info["param_ARD207_OX"] = 50

info["sheetname_ARD207_RED"] = "ARD207 RED" 
info["colums_ARD207_RED"] = ("[muA] EXP-23-DR4288", "[muA] EXP-23-DR4299", "[muA] EXP-23-EA0800", "[muA] EXP-23-EA0802")
info["param_ARD207_RED"] = 50


info["sheetname_ARD207_0V"] = "ARD207 0V" 
info["colums_ARD207_0V"] = ("[muA] EXP-22-DR4258", "[muA] EXP-22-DR4259", "[muA] EXP-22-DR4261")
info["param_ARD207_0V"] = 50

conditions = ("ARD204_OX", "ARD204_RED", "ARD204_0V", "LB_OX", "LB_RED", "LB_0V")
#conditions = ("ARD206_OX", "ARD206_RED", "ARD207_OX", "ARD207_RED", "ARD207_0V")
xls_in = pandas.ExcelFile(info["filename_in"])

with pandas.ExcelWriter("FILTEREDCURRENT.xlsx") as writer:
    for condition in conditions:
        filteredcurrents = {}

        df = pandas.read_excel(xls_in, sheet_name=info["sheetname" + "_" + condition])
        time = pandas.DataFrame(df, columns=["t [sec]"])
        time = time.to_numpy().flatten() 
        
        filteredcurrents["t [sec]"] = time
        
        for column in info["colums" + "_" + condition]:
            current = pandas.DataFrame(df, columns=[column])
            current = current.to_numpy().flatten()
            filteredcurrent = savgol_filter(current, info["param" + "_" + condition], 3)
            filteredcurrents[column] = filteredcurrent
        
        df_out = pandas.DataFrame(filteredcurrents)

        df_out.to_excel(writer, sheet_name=info["sheetname" + "_" + condition] )
    




