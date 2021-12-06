
# imports
import csv
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr #and one more for the creation of a new field


def main(file_path, file_name, timestamp):
    # startup message
    start_msg = f"... {timestamp}: starting conversion (csv to shp) for {file_name}"
    print(start_msg)
    # variables
    input_file = file_path
    EPSG_code = "32632"
    delimiter = ";"
    export_shp = f"/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering/02_konvertert/{timestamp}_{file_name[:-4]}.shp"

    spatialReference = osgeo.osr.SpatialReference() #will create a spatial reference locally to tell the system what the reference will be
    spatialReference.ImportFromEPSG(int(EPSG_code)) #here we define this reference to be the EPSG code
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') # will select the driver for our shp-file creation.
    shapeData = driver.CreateDataSource(export_shp) #so there we will store our data
    layer = shapeData.CreateLayer('layer', spatialReference, osgeo.ogr.wkbPoint) #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn() # gets parameters of the current shapefile
    index = 0

    with open(input_file, 'r') as csvfile:
        readerDict = csv.DictReader(csvfile, delimiter=delimiter)
        for field in readerDict.fieldnames:
            new_field = ogr.FieldDefn(field, ogr.OFTString) #we will create a new field with the content of our header
            layer.CreateField(new_field)
        for row in readerDict:
            # print(row['Pointname'], row['Pointcode'])
            point = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
            point.AddPoint(float(row['E']), float(row['N']), float(row['H'])) #as Strings, so we convert them
            feature = osgeo.ogr.Feature(layer_defn)
            feature.SetGeometry(point) #set the coordinates
            feature.SetFID(index)
            for field in readerDict.fieldnames:
                i = feature.GetFieldIndex(field)
                feature.SetField(i, row[field])
            layer.CreateFeature(feature)
            index += 1
    shapeData.Destroy() #lets close the shapefile

    # success message
    success_msg = "... file succesfully converted."
    print(success_msg)

    # repeat for arkiv (ugly...)

    export_shp = f"/Users/OAS/Dropbox/Savicon AS/Drenering/konvertering/03_arkiv/csv_to_shp/{timestamp}_{file_name[:-4]}.shp"

    spatialReference = osgeo.osr.SpatialReference() #will create a spatial reference locally to tell the system what the reference will be
    spatialReference.ImportFromEPSG(int(EPSG_code)) #here we define this reference to be the EPSG code
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') # will select the driver for our shp-file creation.
    shapeData = driver.CreateDataSource(export_shp) #so there we will store our data
    layer = shapeData.CreateLayer('layer', spatialReference, osgeo.ogr.wkbPoint) #this will create a corresponding layer for our data with given spatial information.
    layer_defn = layer.GetLayerDefn() # gets parameters of the current shapefile
    index = 0

    with open(input_file, 'r') as csvfile:
        readerDict = csv.DictReader(csvfile, delimiter=delimiter)
        for field in readerDict.fieldnames:
            new_field = ogr.FieldDefn(field, ogr.OFTString) #we will create a new field with the content of our header
            layer.CreateField(new_field)
        for row in readerDict:
            # print(row['Pointname'], row['Pointcode'])
            point = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
            point.AddPoint(float(row['E']), float(row['N']), float(row['H'])) #as Strings, so we convert them
            feature = osgeo.ogr.Feature(layer_defn)
            feature.SetGeometry(point) #set the coordinates
            feature.SetFID(index)
            for field in readerDict.fieldnames:
                i = feature.GetFieldIndex(field)
                feature.SetField(i, row[field])
            layer.CreateFeature(feature)
            index += 1
    shapeData.Destroy() #lets close the shapefile
