import geopandas as gpd

def main(file_path, file_name, timestamp):

    # startup message
    start_msg = f"... {timestamp}: starting conversion (shp to dxf) for {file_name}"
    print(start_msg)

    # Set filepath (fix path relative to yours)
    fp = file_path

    # Read file using gpd.read_file()
    data = gpd.read_file(fp)

    # save to konvertert
    print("... saving to folder konvertert")
    data.geometry.to_file(f"/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering/02_konvertert/{timestamp}_{file_name[:-4]}.dxf", driver="DXF")

    # save to arkiv
    print("... saving to arkiv")
    data.geometry.to_file(f"/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering/03_arkiv/shp_to_dxf/{timestamp}_{file_name[:-4]}.dxf", driver="DXF")

    # success message
    success_msg = "... file succesfully converted."
    print(success_msg)
