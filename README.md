# gdal-conversion-watchdog
Collection of scripts performing common gdal/osgeo conversion tasks, wrapped in a simple watchdog and performing some basic logging.

This is a watchdog I threw together to help an agricultural contractor perform common conversion tasks for files used in agricultural applications more quickly and easily than would be possible using Farm Works or other specialized software. 
The following conversions are automatically performed upon discovery of the respective file format in the watched folder:
- .csv to .shp
- .shp to .dxf (more shapefile variations are required for this to work)
- .tif to .csv

Note: This has not been adjusted for general use, i.e. filepaths will have to be adjusted for this to work. Running the script(s) from an anaconda environment should help solve dependency issues (gdal, osgeo, geopandas). Confirmed working configuration: Gdal 3.3.3, conda 4.10.3, python 3.9.7.
