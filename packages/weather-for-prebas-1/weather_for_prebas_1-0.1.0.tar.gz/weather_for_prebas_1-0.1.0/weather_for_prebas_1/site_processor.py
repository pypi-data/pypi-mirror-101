#!/usr/bin/env python

import pdb
import csv
import logging
import argparse
import requests

import pandas as pd 
import numpy as np 

format   = 'csv' # fmt
timespan = 'd'   # tspan
dataset  = 'METO-HC_HadRM3Q0_A1B_HadCM3Q0_DM_25km' # dts
asessment_report = 4 # ar
mode    = 'hisafe'   # mod
url     = 'http://www.isa.ulisboa.pt/proj/clipick/climaterequest_fast.php' 

CO2= 380

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)



def transform_row(row_raw):
    row = [float(i) for i in row_raw.split(",")]
    PAR = row[7]*0.4278*4.56
    TAir = (row[3] + row[4])/2
    SVP = 610.7*10**(7.5*TAir/(237.3+TAir))
    VPD = SVP*(1-(row[5]+row[6])/2/100)/1000
    Precip = row[8]

    return PAR, TAir, VPD, Precip


string_date = {
    'sy': str, 
    'sm': int,
    'sd': int,
    'ey': str,
    'em': int,
    'ed': int
}


def make_request(df):

    response = requests.get(url, params={
        'lat': df.lat,
        'lon': df.lon,
        'fmt': format,
        'sy': df.sy,
        'sm': df.sm,
        'sd': df.sd,
        'ey': df.ey,
        'em': df.em,
        'ed': df.ed,
        'tspan': timespan,
        'dts': dataset,
        'ar': asessment_report,
        'mod': mode
    })

    return response


def get_data_from_clipick(sites, output_path):

    with open(output_path, 'w') as sink:
        sink_writer = csv.writer(sink)
        sink_writer.writerow(["clim_id", "PAR", "TAir", "VPD", "Precip", "CO2"])

        not_working = []

        sites_df = pd.read_csv(sites, dtype=string_date)
        sites_count = sites_df.shape[0]

        for index, df in sites_df.iterrows():
            
            response = make_request(df)

            '''# FILENAME: 3.123,965.34_2019.07-2020.07.csv
            lat_lon    = f'{df.lat:.3f},{df.lon:.3f}'; 
            start_date = f'{df.sy.strip()}.{df.sm:02}.{df.sd:02}'
            end_date   = f'{df.ey.strip()}.{df.em:02}.{df.ed:02}'
            filename   = f'{lat_lon}__{start_date}-{end_date}'''
            
            items = response.iter_lines()

            #skip headers
            headers = next(items)

            if not headers.decode('utf-8').lower() == 'day,month,year,tasmax,tasmin,hursmax,hursmin,rss,pr,wss':
                not_working.append(index)
                continue

            for row in items:
                row = row.decode('utf-8')

                #skip empty entries (what is the cause?)
                if row == '':
                    continue

                PAR, TAir, VPD, Precip = transform_row(row)
                sink_writer.writerow([index+1, PAR, TAir, VPD, Precip, CO2])

            if 100*index % sites_count == 0:
                logging.info(f"{round(100*index/sites_count)}% processed.")


    logging.info(f"Weather data for {sites_count-len(not_working)} sites written to {output_path}")
    if not_working:
        logging.warning(f"Data could not be acquired for the following sites:\n{not_working}")  


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get weather data from Clipick')
    parser.add_argument('--sites', type=str,
                        help='a CSV file containing lat,lon and dates for each site')
    parser.add_argument('--output', type=str,
                        help='path where the output will be written')

    args = parser.parse_args()

    get_data_from_clipick(args.sites, args.output)

    
