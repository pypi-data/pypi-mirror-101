import pytz
import datetime as dt
from . import convtime

import re
import logging
import os

import requests
from pathlib import Path

import xarray as xr
import pandas as pd


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def fn_to_utc(filename):
    return dt.datetime.strptime(re.sub('.*_', '', filename).replace('.nc', ''), "%Y%m%d%H%M")

class dataplatform():
    def __init__(self,
                 api_keys,
                 start = None,  # local
                 end = None,    # local,
                 dataset_name = "Actuele10mindataKNMIstations", 
                 dataset_version = "2", 
                 max_keys = "500",
                 api_url = "https://api.dataplatform.knmi.nl/open-data",
                 api_version = "v1",
                 tz = pytz.timezone('Europe/Amsterdam'),
                 tf = "%Y%m%d%H%M"
                ):
        self.api_keys = api_keys
        self.tz = tz
        self.tf = tf

        self.key_index = 0
        self.max_keys = max_keys
        self.api = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files"
          
        start = start or dt.datetime.now(tz) - dt.timedelta(minutes = 10)
        self.req_from = convtime.local_to_utc(start, self.tz)
        
        self.end = end or (start + dt.timedelta(days = 1)).replace(hour = 0, minute = 0, second = 0)
        if self.end.tzinfo is None:
            self.end = tz.localize(self.end) 

        self.files = None
        
    def knmi_req(self, url, params = None, error = 'Request failed'):
        response = requests.get(
            url,
            headers = {"Authorization": self.api_keys[self.key_index]},
            params = params
        )
        
        result = response.json()
        if response.status_code != 200:
            if 'error' in result:
                logger.error(error)
                logger.error(response.text)
                
                if self.key_index >= len(self.api_keys):
                    logger.error("No more api key left to use")
                logger.info("Another api key is used. Expected error: current key has exceeded the quota (50/hr)")
                self.key_index = self.key_index + 1
                result = self.knmi_req(url, params, error)
                
                   
        return result
    
    # Use list files request
    def list_files(self):
        
        start_after_filename_prefix = f"KMDS__OPER_P___10M_OBS_L2_{convtime.round_10min(self.req_from).strftime(self.tf)}"
        list_files = self.knmi_req(
            url = self.api,
            params = {"maxKeys": self.max_keys, "startAfterFilename": start_after_filename_prefix},
            error = "Unable to list files in the dataset"
        )
        dataset_files = list_files.get("files")
        self.files = dataset_files
        
        return dataset_files
    
    # Retrieve file
    def download_file(self, filename):
        
        logger.info(f"Retrieve file with name: {filename}")
        download_url = self.knmi_req(
            url = f"{self.api}/{filename}/url",
            error = "Unable to retrieve download url for file"
        ).get("temporaryDownloadUrl")
        
        dataset_file_response = requests.get(download_url)
        if dataset_file_response.status_code != 200:
            logger.error("Unable to download file using download URL")
            logger.error(dataset_file_response.text)

        # Write dataset file to disk
        path = Path('/tmp/' + filename)
        path.write_bytes(dataset_file_response.content)
        logger.info(f"Successfully downloaded dataset file to {path}")
        
        return path
    
    # Open as dataframe and format name
    def get_df(self, filename):
        
        time = convtime.utc_to_local(fn_to_utc(filename), self.tz)
        print(time)
        
        path = self.download_file(filename)
        ds = xr.open_dataset(path)
        df = ds.to_dataframe().reset_index()
        
        df.drop(columns = ["iso_dataset", "product", "projection"], inplace = True)
        df.columns = [re.sub('[^A-Za-z0-9]+', '', col).lower() for col in df.columns]
        df = df.rename(columns = {"time" : "time_utc"}).assign(
            date = time.date(),
            hour = time.hour,
            minute = time.minute,
            station = df.station.astype('int')
        )
            
        # Remove file
        ds.close()
        os.remove(path)
        
        return df.loc[df.station < 70000]
    
    def process(self, timestamps = None, last = False): # timestamps in utc
        
        if not self.files:
            # have to do stuffs 
            self.list_files()
        
        if timestamps:
            fn = [f.get('filename') for f in self.files if fn_to_utc(f.get('filename')) in timestamps]
        else:
            fn = [f.get('filename') for f in self.files if convtime.utc_to_local(fn_to_utc(f.get('filename')), self.tz) < self.end]
            if last:
                fn = [max(fn)]
        
        ldf = list(map(self.get_df, fn))
        if ldf:
            return pd.concat(ldf)
    
