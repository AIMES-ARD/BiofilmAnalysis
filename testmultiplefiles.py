import numpy as np
import pandas as pd
from aicsimageio import AICSImage
import os

folder = "./DATA/SH1000 test"
output_xlsx = "SH1000 test.xlsx"

# Find all czi files in the folder:
czi_files = [f for f in os.listdir(folder) if f.endswith('.czi')]


# Alternatively, list specific files:
# czi_files = [
#     "SH1000 Ebba680+ R1 airyscan.czi",
#     "SH1000 Ebba680+ R2 airyscan.czi",
#     # etc
#     ]


# print(f"Found {len(czi_files)} .czi files.")

with pd.ExcelWriter(output_xlsx) as writer:
    for czi_file in czi_files:
        # print(f"Processing file: {czi_file}")
        czi_path = os.path.join(folder, czi_file)
        img = AICSImage(czi_path)
        RED =  img.get_image_data("ZYX", C=0, S=0, T=0)
        GREEN =  img.get_image_data("ZYX", C=1, S=0, T=0)

        data = {}

        intensityperslice_red = []
        intensityperslice_green = []
        for s in range(np.shape(GREEN)[0]):
            intensityperslice_red.append(RED[s, :, :].sum())
            intensityperslice_green.append(GREEN[s, :, :].sum())

        data["Ebba"] = intensityperslice_red
        data["GFP"] = intensityperslice_green
        
        df_out = pd.DataFrame(data)
        sheet_name = os.path.splitext(czi_file)[0]
        df_out.to_excel(writer, sheet_name = sheet_name) 


