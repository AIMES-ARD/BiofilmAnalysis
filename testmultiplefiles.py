import numpy as np
import pandas as pd
from aicsimageio import AICSImage
import os

folder = "./DATA/SH1001"
output_xlsx = "Normalized SH1001 intensities.xlsx"

# Find all czi files in the specified folder:
czi_files = [f for f in os.listdir(folder) if f.endswith('.czi')]


# Alternatively, find all specific files manually listed:
# czi_files = [
#     "SH1000 Ebba680+ R1 airyscan.czi",
#     "SH1000 Ebba680+ R2 airyscan.czi",
#     # etc
#     ]


# print(f"Found {len(czi_files)} .czi files.")

czi_files.sort()

with pd.ExcelWriter(output_xlsx) as writer:
    for czi_file in czi_files:
        print(f"Processing file: {czi_file}")
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

        # data["Ebba"] = intensityperslice_red
        # data["GFP"] = intensityperslice_green

        max_red = np.max(intensityperslice_red)
        max_green = np.max(intensityperslice_green)
        intensityperslice_red_norm = intensityperslice_red/max_red
        intensityperslice_green_norm = intensityperslice_green/max_green

        i_max_red = np.argmax(intensityperslice_red)
        i_max_green = np.argmax(intensityperslice_green)
        aligned_intensityperslice_red = np.zeros((120))
        aligned_intensityperslice_green = np.zeros((120))
        # print(np.shape(aligned_intensityperslice_red))

        x_diff_red = 60 - i_max_red
        x_diff_green = 60 - i_max_green

        # print(aligned_intensityperslice_red)

        try:
            aligned_intensityperslice_red[x_diff_red:x_diff_red + len(intensityperslice_red)] = intensityperslice_red_norm
            aligned_intensityperslice_green[x_diff_green:x_diff_green + len(intensityperslice_green)] = intensityperslice_green_norm
            # print(aligned_intensityperslice_red)
    
        except ValueError:
            print(np.shape(intensityperslice_red))
            print(np.shape(intensityperslice_green))
            print(i_max_red)
            print(i_max_green)


        data["Ebba"] = aligned_intensityperslice_red
        data["GFP"] = aligned_intensityperslice_green


        df_out = pd.DataFrame(data)
        sheet_name = os.path.splitext(czi_file)[0]
        df_out.to_excel(writer, sheet_name = sheet_name) 


