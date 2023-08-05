# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04b_nrt.ipynb (unless otherwise specified).

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
from .core import filter_files, ls, Path, InOutPath, ProjectPath
from .geo import Region
from .data import *
from .predict import predict_nrt
from .web import array2png
from fire_split.core import split_fires, save_data, to_polygon
import pdb
Path.ls = ls

# Cell
class RunManager():
    def __init__(self, project_path:ProjectPath, region, time='today',
                 product:str='VIIRS750', days=64):
        self.path    = project_path
        self.time    = self.init_time(time)
        self.product = product
        self.region  = region
        self.days    = days

    @property
    def R(self):
         return Region.load(f'{self.path.config}/R_{self.region}.json')

    def init_time(self, time):
        if time == 'today':
            time = pd.Timestamp(datetime.date.today())
        elif time == 'yesterday':
            time = pd.Timestamp(datetime.date.today())-pd.Timedelta(days=1)
        return time

    def last_n_days(self, time:pd.Timestamp, days):
        return pd.date_range(start=time-pd.Timedelta(days=days-1), periods=days,
                              freq='D')

    def check_data(self):
        "Check existing and missing files in dataset folder."
        times = self.last_n_days(self.time, self.days)
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
            start = self.last_n_days(self.time, self.days)[0]
        else:
            start = pd.Timestamp(files[-1].stem.split('_')[-1])+pd.Timedelta(days=1)
        start = start.strftime('%Y-%m-%d 00:00:00')
        end = self.time.strftime('%Y-%m-%d 23:59:59')
        return start, end

    def update_hotspots(self, location, mode='7d', save=True):
        """Update hotspots file with new data.
          location is according to the data url naming format
          mode can be on of: 24h, 48h, 7d"""
        url = f'https://firms.modaps.eosdis.nasa.gov/' \
                   f'active_fire/viirs/text/VNP14IMGTDL_NRT_{location}_{mode}.csv'
        files = self.path.hotspots.ls(include=['.csv', f'hotspots{self.region}'])
        frp = [pd.read_csv(f) for f in files]
        frp = pd.concat([*frp, pd.read_csv(url)], axis=0, sort=False
                        ).drop_duplicates().reset_index(drop=True)
        if save:
            frp.to_csv(self.path.hotspots/f'hotspots{self.region}.csv', index=False)
            print(f'hotspots{self.region}.csv updated')
        else: return frp

    def download_viirs(self):
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
            viirs_downloader_list1 = viirs_downloader1.split_times()
            viirs_downloader_list2 = viirs_downloader2.split_times()
            viirs_downloader_list = [*viirs_downloader_list1, *viirs_downloader_list2]

        else: raise NotImplementedError(f'Not implemented for {self.product}.')

        run_all(viirs_downloader_list, self.path.ladsweb)

    def preprocess_dataset_750(self, max_size=None, max_workers=1):
        "Apply pre-processing to the rawdata and saves results in dataset directory."
        paths = InOutPath(f'{self.path.ladsweb}', f'{self.path.dataset}')
        R = self.R.new()
        bands = ['Reflectance_M5', 'Reflectance_M7', 'Reflectance_M10', 'Radiance_M12',
                 'Radiance_M15', 'SolarZenithAngle', 'SatelliteZenithAngle']
        print('\nPre-processing data...')
        viirs = Viirs750Dataset(paths, R, bands=bands)
        merge_tiles = MergeTiles('SatelliteZenithAngle', ignore=['R'])
        mir_calc = MirCalc('SolarZenithAngle', 'Radiance_M12', 'Radiance_M15')
        rename = BandsRename(['Reflectance_M5', 'Reflectance_M7'], ['Red', 'NIR'])
        bfilter = BandsFilter(['Red', 'NIR', 'MIR', 'R'])
        act_fires = ActiveFiresLog(f'{self.path.hotspots}/hotspots{self.region}.csv')
        bfilter2 = BandsFilter(['Red', 'NIR', 'MIR', 'FRP'])
        if max_size is None:
            proc_funcs = [BandsAssertShape(), merge_tiles,
                          mir_calc, rename, bfilter1, act_fires, bfilter2]
        else:
            proc_funcs = [merge_tiles, mir_calc, rename, bfilter1,
                          act_fires, bfilter2]
        viirs.process_all(proc_funcs=proc_funcs, max_size=max_size, max_workers=max_workers)

    def preprocess_dataset_375(self, max_size=None, max_workers=1):
        "Apply pre-processing to the rawdata and saves results in dataset directory."
        paths = InOutPath(f'{self.path.ladsweb}', f'{self.path.dataset}')
        R = self.R.new()
        bands = ['Reflectance_I1', 'Reflectance_I2', 'Reflectance_I3',
                 'Radiance_I4', 'Radiance_I5', 'SolarZenithAngle', 'SatelliteZenithAngle']
        print('\nPre-processing data...')
        viirs = Viirs375Dataset(paths, R, bands=bands)
        interpAng = InterpolateAngles(R.new(pixel_size=0.1), R,
                              ['SolarZenithAngle', 'SatelliteZenithAngle'])
        merge_tiles = MergeTiles('SatelliteZenithAngle', ignore=['R'])
        mir_calc = MirCalc('SolarZenithAngle', 'Radiance_I4', 'Radiance_I5')
        rename = BandsRename(['Reflectance_I1', 'Reflectance_I2'], ['Red', 'NIR'])
        bfilter1 = BandsFilter(['Red', 'NIR', 'MIR', 'R'])
        act_fires = ActiveFiresLog(f'{self.path.hotspots}/hotspots{self.region}.csv')
        bfilter2 = BandsFilter(['Red', 'NIR', 'MIR', 'FRP'])
        if max_size is None:
            proc_funcs = [interpAng, BandsAssertShape(), merge_tiles,
                          mir_calc, rename, bfilter1, act_fires, bfilter2]
        else:
            proc_funcs = [interpAng, merge_tiles, mir_calc, rename, bfilter1,
                          act_fires, bfilter2]
        viirs.process_all(proc_funcs=proc_funcs, max_size=max_size, max_workers=max_workers)

    def preprocess_dataset(self, max_size=None, max_workers=1):
        if self.product == 'VIIRS750':
            self.preprocess_dataset_750(max_size=max_size, max_workers=max_workers)
        elif self.product == 'VIIRS375':
            self.preprocess_dataset_375(max_size=max_size, max_workers=max_workers)
        else: raise NotImplementedError(f'Not implemented for {self.product}.')

    def init_model_weights(self, weight_files:list):
        "Downloads model weights if they don't exist yet on config directory."
        local_files = []
        for w in weight_files:
            file_save = self.path.config/w
            if not file_save.is_file():
                print(f'Downloading model weights {w}')
                url = f'https://github.com/mnpinto/banet_weights/raw/master/model/{w}'
                file = requests.get(url)
                open(str(file_save), 'wb').write(file.content)
            local_files.append(file_save)
        return local_files

    def get_preds(self, weight_files:list, threshold=0.5, save=True, max_size=2000):
        "Computes BA-Net predictions ensembling the models in the weight_files list."
        local_files = self.init_model_weights(weight_files)
        iop = InOutPath(self.path.dataset, self.path.outputs, mkdir=False)
        region = self.R.new()
        predict_nrt(iop, self.time, local_files, region, threshold=threshold,
                    save=save, max_size=max_size, product=self.product)

    def postprocess(self, filename, threshold=0.5, interval_days=2, interval_pixels=2,
                    min_size_pixels=25, area_epsg=None, keys=['burned', 'date'],
                    geotiff_only=False, padding=1):
        "Computes tifs and shapefiles from outputs."
        data = sio.loadmat(self.path.outputs/f'{filename}.mat')
        times = pd.DatetimeIndex([pd.Timestamp(str(o)) for o in data['times']])
        unique_years = times.year.unique()
        if len(unique_years) > 2: raise NotImplementedError(
            'Not implemented for more than 2 years range')
        burned = data[keys[0]]
        date = data[keys[1]]
        I = burned < threshold
        date[I] = np.nan
        It = date[date>=0].astype(np.uint16)
        if len(unique_years) > 1:
            m = (times.year[It] == unique_years[1])*pd.Timestamp(f'{unique_years[1]}-12-31').dayofyear
        else: m = 0
        date[date>=0] = times[It].dayofyear + m
        date[np.isnan(date)] = 0
        date = date.astype(np.uint16)
        burned = (burned*255).astype(np.uint8)
        region = self.R.new()
        if geotiff_only:
            raster = np.array([burned, date])
            save_data(self.path.web/f'{filename}.tif', raster, crs=region.crs,
                                   transform=region.transform)
        else:
            labels, df = split_fires(date, interval_days=interval_days,
                         interval_pixels=interval_pixels,
                         min_size_pixels=min_size_pixels)
            burned[labels==0] = 0
            date[labels==0] = 0
            raster = np.array([burned, date])
            save_data(self.path.web/f'{filename}.tif', raster, crs=region.crs,
                                   transform=region.transform)
            for i in range(labels.max()):
                l = (i+1)
                f = labels == l
                args = np.argwhere(f)
                lon, lat = region.coords()
                (rmin, cmin), (rmax, cmax) = args.min(0), args.max(0)
                rmax += 1
                cmax += 1
                rmin = max(rmin, 1)
                cmin = max(cmin, 1)
                lat_r = lat[rmin-padding:rmax+padding]
                lon_r = lon[cmin-padding:cmax+padding]
                tfm = rasterio.Affine(region.pixel_size, 0, lon_r.min(), 0, -region.pixel_size, lat_r.max())
                burned_r = data[keys[0]][rmin-padding:rmax+padding, cmin-padding:cmax+padding].copy().astype(np.float16)
                date_r =  data[keys[1]][rmin-padding:rmax+padding, cmin-padding:cmax+padding].copy().astype(np.float16)
                burned_r[f[rmin-padding:rmax+padding, cmin-padding:cmax+padding]==0] = np.nan
                date_r[f[rmin-padding:rmax+padding, cmin-padding:cmax+padding]==0] = np.nan

                burned_r = burned_r*255
                burned_r[np.isnan(burned_r)] = 0
                burned_r = burned_r.astype(np.uint16)
                date_r[np.isnan(date_r)] = 0
                date_r = date_r.astype(np.uint16)
                raster = np.array((burned_r, date_r))

                (self.path.web/'events').mkdir(exist_ok=True)
                save_data(self.path.web/'events'/f'{filename}_{l}.tif',
                          raster, crs=region.crs, transform=tfm)
                im = array2png(burned_r, cmap='RdYlGn_r')
                im.save(self.path.web/'events'/f'{filename}_{l}_cl.png')
                im = array2png(date_r, cmap='jet')
                im.save(self.path.web/'events'/f'{filename}_{l}_bd.png')

            df = to_polygon(labels, region.crs, region.transform, df, area_epsg=area_epsg)
            df['area_ha'] = df['area_ha'].astype(np.uint32)
            df.to_file(self.path.web/f'{filename}.shp')
            df.to_file(self.path.web/f'{filename}.json', driver='GeoJSON')