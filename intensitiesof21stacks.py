import numpy as np
import pandas as pd
from aicsimageio import AICSImage
import os

folder = "./DATA/SH1002-pSGFPS1"
output_xlsx = "Normalized SH1002 21 intensities.xlsx"

# Number of stacks before and after the maximum intensity
num_stacks = 10

# Find all czi files in the specified folder:
czi_files = [f for f in os.listdir(folder) if f.endswith('.czi')]

# Alternatively, find all specific files manually listed:
# czi_files = [
#     "SH1000_Ebba680+_R1_airyscan.czi",
#     "SH1000_Ebba680+_R2_airyscan.czi",
#     # etc
# ]

czi_files.sort()

with pd.ExcelWriter(output_xlsx) as writer:
    for czi_file in czi_files:
        print(f"Processing file: {czi_file}")
        czi_path = os.path.join(folder, czi_file)
        img = AICSImage(czi_path)
        RED = img.get_image_data("ZYX", C=0, S=0, T=0)
        GREEN = img.get_image_data("ZYX", C=1, S=0, T=0)

        data = {}

        intensityperslice_red = []
        intensityperslice_green = []
        for s in range(np.shape(GREEN)[0]):
            intensityperslice_red.append(RED[s, :, :].sum())
            intensityperslice_green.append(GREEN[s, :, :].sum())

        max_intensity_index = np.argmax(intensityperslice_red)

        # Calculate the range of indices
        start_index = max(0, max_intensity_index - num_stacks)
        end_index = min(len(intensityperslice_red), max_intensity_index + num_stacks + 1)

        used_stacks_before = max_intensity_index - start_index
        used_stacks_after = end_index - max_intensity_index - 1

        print(f"Using {used_stacks_before} stacks before and {used_stacks_after} stacks after the maximum intensity for file {czi_file}.")

        selected_red_intensities = intensityperslice_red[start_index:end_index]
        selected_green_intensities = intensityperslice_green[start_index:end_index]

        max_red = np.max(selected_red_intensities)
        max_green = np.max(selected_green_intensities)
        selected_red_intensities_norm = np.array(selected_red_intensities) / max_red
        selected_green_intensities_norm = np.array(selected_green_intensities) / max_green

        data["Ebba"] = selected_red_intensities_norm
        data["GFP"] = selected_green_intensities_norm

        df_out = pd.DataFrame(data)
        sheet_name = os.path.splitext(czi_file)[0]
        df_out.to_excel(writer, sheet_name=sheet_name)

print(f"Results saved to {output_xlsx}.")
