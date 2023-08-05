import logging
import pdb
import os
import sys
import argparse
import shapely
import geopandas as gpd

#from .sites import create_sites_file
#from sites import create_sites_file
import sites.create_sites_file
#from .site_processor import get_data_from_clipick
import site_processor.get_data_from_clipick
logging.getLogger().setLevel(logging.INFO)

clipick_extent_wkt = "POLYGON ((23.47841578340817 34.39788005192901, 14.25327875377249 35.33928230717498, 13.13483184162019 36.22363567957447, 11.05400037715079 36.14560449965687, -6.893171003897777 34.66301208122243, -9.130064828202382 35.13119916072804, -24.93076907914224 63.08858354916435, -25.45991436426534 66.02827957762601, -24.34282987344992 66.96898230673375, -20.52122503644976 66.85139446559528, -19.93328583075743 67.96847895641071, -16.40565059660344 67.20415798901068, 6.999470176817231 65.6193153140163, 14.64163755884682 71.28506009724514, 28.67423801033218 71.94386763017873, 43.29976524145776 69.04511448527094, 45.27618784025852 69.11099523856431, 50.61252885702055 66.40988435353661, 40.31397457104929 58.02929279476642, 37.39889048539511 54.33163580021179, 35.26637930864139 51.35785874639009, 32.39203249604414 46.46751416521121, 30.25958830641831 41.47759476148677, 30.13164165504076 41.0511059235616, 29.06541956022784 36.65827089293239, 28.29773965196255 35.50675103053445, 26.84767760301698 34.39788005192901, 23.47841578340817 34.39788005192901))"

def get_weather_data(aoi_path, sites_path, weather_path, start_date, end_date, step=25):
    #extent_file = os.path.join(sys.path[0], "clipick_extent_wkt.txt")
    #with open(extent_file, "r") as f:
    #    wkt_geom = f.read()
    #    clipick_extent = shapely.wkt.loads(wkt_geom) 
    clipick_extent = shapely.wkt.loads(clipick_extent_wkt) 
    clipick_extent_gdf = gpd.GeoDataFrame({"id" : [1], "geometry": [clipick_extent]}, crs="EPSG:4326")

    aoi = gpd.read_file(aoi_path)

    if aoi.crs.to_epsg() != 4326:
        aoi = aoi.to_crs(epsg=4326)

    if not aoi.intersects(clipick_extent).any():
        raise Exception("Area of interest not covered by Clipick")
    
    if not aoi.within(clipick_extent).all():
        intersection_area = gpd.overlay(aoi, clipick_extent_gdf, how="intersection").geometry.area
        aoi_covered = round((100*intersection_area/aoi.area).values[0], 2)
        logging.warning(f" Only {aoi_covered}% of AoI covered by Clipick")
        aoi = gpd.clip(aoi, clipick_extent)

    create_sites_file(aoi, sites_path, start_date, end_date, step)
    get_data_from_clipick(sites_path, weather_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a grid of points')
    parser.add_argument('--aoi', type=str, required=True,
                        help='file with AOI')
    parser.add_argument('--sites_path', type=str, required=True,
                        help='path to where file with sites will be created')
    parser.add_argument('--weather_path', type=str, required=True,
                        help='path to where file with weather will be created')
    parser.add_argument('--step', type=float, default=25,
                        help='density of the grid in kilometers, defaults to 25')
    parser.add_argument('--start_date', type=str, required=True,
                        help='Starting date, either in format dd/mm/yyyy or just year (1/1)')
    parser.add_argument('--end_date', type=str, required=True,
                        help='End date, either in format dd/mm/yyyy or just year (31/12)')
    args = parser.parse_args()

    get_weather_data(args.aoi,
         args.sites_path,
         args.weather_path,
         args.start_date,
         args.end_date,
         args.step)

