"""
Name: Generate a point grid within polygon
Author: Jan Pisl
Description: Generate a grid of points within
a polygon given as shapefile or similar. Generates
also points that are within a buffer of the polygon.
The points have an approximately equal distance in kilometers.

Conversion between kilometers and lat/lon are done using
the following formulas:
Latitude: 1 deg = 110.574 km
Longitude: 1 deg = 111.320*cos(latitude) km
https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance#:~:text=Latitude%3A%201%20deg%20%3D%20110.574%20km


Example of use:

python sites.py --shape test_aoi.shp --output_path sites_test.csv --start_date 2014 --end_date 2014
"""

import logging
import math
import csv
import argparse

import utm
import numpy as np
import geopandas as gpd
from shapely.geometry import Point


lat_conversion_const = 110.574
lon_conversion_const = 111.320


def create_grid(gdf, step=25):

    if not gdf.crs.to_epsg() == 4326:
        gdf = gdf.to_crs(epsg=4326)

    #TODO: handle multiple geometries
    if gdf.shape[0] > 1:
        raise NotImplementedError("Multiple shapes not handled yet.")

    # add a buffer of 2 steps in latitudial direction.
    # not perfect but likely good enough
    buffered_shape = gdf.loc[0].geometry.buffer(2*step/lat_conversion_const)

    min_lon, min_lat, max_lon, max_lat = buffered_shape.bounds

    lat, lon = min_lat, min_lon

    coords = []
    
    while lat < max_lat:
        while lon < max_lon:
            lon += step/(lon_conversion_const*math.cos(lat*2*math.pi/360))
            coords.append((lon, lat))
            
        lat += step/lat_conversion_const
        lon = min_lon

    filtered = [i for i in coords if buffered_shape.contains(Point(i))]

    return filtered


def get_headers(data):
    columns = len(data[0])
    if columns == 2:
        headers = ['lon', 'lat']
    elif columns == 8:
        headers = ['lon', 'lat', 'sy', 'sm', 'sd', 'ey', 'em', 'ed']
    else:
        raise Exception("Failed to determine what headers to use")

    return headers


def write_points_to_csv(grid, out_path):
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        headers = get_headers(grid)
        writer.writerow(headers)
        writer.writerows(grid)

    logging.info(f"{len(grid)} points written to {out_path}")


def parse_date(date):
    if "/" in str(date):
        try:
            day, month, year = date.split("/")
        except ValueError:
            raise Exception(f"Invalid date: {date}")
    else:
        day, month, year = None, None, date

    return year, month, day


def add_dates(point_list, start_date, end_date):
    start_date = parse_date(start_date)
    if start_date[2] is None:
        start_date = (start_date[0], 1, 1)
    
    end_date = parse_date(end_date)
    if end_date[2] is None:
        end_date = (end_date[0], 12, 31)

    dated_points = [(*point, *start_date, *end_date) for point in point_list]

    return dated_points


def create_sites_file(aoi, out_path, start_date, end_date, step):

    grid_points = create_grid(aoi, step)

    points_with_dates = add_dates(grid_points, start_date, end_date)

    write_points_to_csv(points_with_dates, out_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a grid of points')
    parser.add_argument('--shape', type=str,
                        help='file with AOI')
    parser.add_argument('--output_path', type=str,
                        help='path to file with sites that will be created')
    parser.add_argument('--step', type=float, default=25,
                        help='density of the grid in kilometers, defaults to 25')
    parser.add_argument('--start_date', type=str,
                        help='Starting date, either in format dd/mm/yyyy or just year (1/1)')
    parser.add_argument('--end_date', type=str,
                        help='End date, either in format dd/mm/yyyy or just year (31/12)')
    args = parser.parse_args()

    create_sites_file(gpd.read_file(args.shape), args.step, args.start_date, args.end_date, args.output_path)

