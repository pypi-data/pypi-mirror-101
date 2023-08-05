# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04c_historical.ipynb (unless otherwise specified).

__all__ = ['RunManager']

# Cell
import pandas as pd
import numpy as np
import scipy.io as sio
import rasterio
import requests
import IPython
import matplotlib.pyplot as plt
from nbdev.imports import test_eq
import datetime
from geoget.download import run_all
import banet.nrt
from .core import filter_files, ls, Path, InOutPath, ProjectPath
from .geo import Region
from .data import *
from .predict import predict_time
from fire_split.core import split_fires, save_data, to_polygon
Path.ls = ls

# Cell
class RunManager(banet.nrt.RunManager):
    def __init__(self, project_path:ProjectPath, region:str, times:pd.DatetimeIndex,
                 product:str='VIIRS750'):
        """
        project_path: banet.core.ProjectPath object
        region: name of the region
        times: dates for the first day of month for each month to use
        product: VIIRS750 or VIIRS375
        """
        self.path    = project_path
        self.times   = self.init_times(times)
        self.product = product
        self.region  = region

    def init_times(self, times):
        tstart = times[0] - pd.Timedelta(days=15)
        tstart = pd.Timestamp(f'{tstart.year}-{tstart.month}-01')
        tend = times[-1] + pd.Timedelta(days=75)
        tend = pd.Timestamp(f'{tend.year}-{tend.month}-01') - pd.Timedelta(days=1)
        return pd.date_range(tstart, tend, freq='D')

    def check_data(self):
        "Check existing and missing files in dataset folder."
        times = self.times
        files, missing_files = [], []
        for t in times:
            tstr = t.strftime('%Y%m%d')
            file = self.path.dataset/f'{self.product}{self.region}_{tstr}.nc'
            if file.is_file():
                files.append(file)
            else:
                missing_files.append(file)
        return {'files': files, 'missing_files': missing_files}

    def get_download_dates(self):
        "Find for which new dates the files need to be downloaded."
        files = self.check_data()['files']
        if len(files) == 0:
            start = self.times[0]
        else:
            start = pd.Timestamp(files[-1].stem.split('_')[-1])+pd.Timedelta(days=1)
        start = start.strftime('%Y-%m-%d 00:00:00')
        end = self.times[-1].strftime('%Y-%m-%d 23:59:59')
        return start, end

    def download_viirs(self, maxOrderSize=[1800, 1200]):
        "Download viirs data needed for the dataset."
        tstart, tend = self.get_download_dates()
        region = self.R.new()

        if self.product == 'VIIRS750':
            viirs_downloader = VIIRS750_download(region, tstart, tend)
            viirs_downloader_list = viirs_downloader.split_times()

        elif self.product == 'VIIRS375':
            viirs_downloader1 = VIIRS375_download(region, tstart, tend)
            region.pixel_size = 0.1 # Angles can be interpolated later
            viirs_downloader2 = VIIRS750_download(region, tstart, tend,
                                bands=['SolarZenithAngle', 'SatelliteZenithAngle'])
            viirs_downloader_list1 = viirs_downloader1.split_times(maxOrderSize=maxOrderSize[0])
            viirs_downloader_list2 = viirs_downloader2.split_times(maxOrderSize=maxOrderSize[1])
            viirs_downloader_list = [*viirs_downloader_list1, *viirs_downloader_list2]
        else: raise NotImplementedError(f'Not implemented for {self.product}.')

        run_all(viirs_downloader_list, self.path.ladsweb)

    def get_preds(self, weight_files:list, threshold=0.5, save=True, max_size=2000,
                  filename='data', check_file=False, verbose=False):
        "Computes BA-Net predictions ensembling the models in the weight_files list."
        local_files = self.init_model_weights(weight_files)
        iop = InOutPath(self.path.dataset, self.path.outputs, mkdir=False)
        region = self.R.new()
        predict_time(iop, self.times, local_files, region, threshold=threshold,
                     save=save, max_size=max_size, product=self.product, output=filename,
                      check_file=check_file, verbose=verbose)