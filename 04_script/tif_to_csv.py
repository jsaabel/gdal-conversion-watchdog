from osgeo import gdal
import pandas as pd
import os
# import numpy as np
# import matplotlib.pyplot as plt
folder = "/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering"

def main(file_path, file_name, timestamp):

    # startup message
    start_msg = f"... {timestamp}: starting conversion (tif to csv) for {file_name}"
    print(start_msg)

    print(f"... opening {file_path} with gdal module")
    ds = gdal.Open(file_path)
    print("... starting gdal.Translate")
    xyz = gdal.Translate(f"temp.xyz", ds, options = "-r nearest -tr 6 6")
    xyz = None  # close dataset
    print("... opening dataframe in pandas")
    df = pd.read_csv("temp.xyz", sep = " ", header = None)
    df.columns = ["X", "Y", "Z"]
    # save to 02_konvertert and 03_arkiv
    print("... writing to csv")
    df.to_csv(f"/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering/02_konvertert/{timestamp}_{file_name[:-4]}.csv", sep = ";", header="X;Y;Z", index = False)
    df.to_csv(f"/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering/03_arkiv/tif_to_csv/{timestamp}_{file_name[:-4]}.csv", sep = ";", header="X;Y;Z", index = False)
    # delete temp file
    print("removing tmp file")
    os.remove("temp.xyz")

    # success message
    success_msg = "... file succesfully converted."
    print(success_msg)
    with open(f"{folder}/04_script/log.txt", "a") as f:
        f.write(f"{timestamp}: {success_msg}\n")
