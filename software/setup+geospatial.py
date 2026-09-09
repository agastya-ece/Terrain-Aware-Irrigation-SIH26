# SEGMENT 1: SETUP & GEOSPATIAL DATA INGESTION
import os
import json
import time
import requests
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
from sklearn.ensemble import RandomForestRegressor

TIF_PATH = r"D:\Downloads\irrigation_index.tif"

def load_geotiff_index(filepath):
    with rasterio.open(filepath) as src:
        raw_data = src.read(1).astype(np.float32)
        transform = src.transform
        bounds = src.bounds
        crs = src.crs

    valid_mask = (raw_data > -1000.0) & (~np.isnan(raw_data))
    clean_data = np.where(valid_mask, raw_data, np.nan)
    median_val = np.nanmedian(clean_data)
    clean_data = np.nan_to_num(clean_data, nan=median_val)
    
    min_v, max_v = float(clean_data.min()), float(clean_data.max())
    norm_index = (clean_data - min_v) / (max_v - min_v + 1e-6)

    return {
        "raw_grid": clean_data,
        "norm_grid": norm_index,
        "shape": clean_data.shape,
        "bounds": bounds,
        "transform": transform,
        "crs": str(crs),
        "min": min_v,
        "max": max_v
    }

tif_meta = load_geotiff_index(TIF_PATH)
print(f"GeoTIFF Loaded: Shape {tif_meta['shape']} | Range [{tif_meta['min']:.2f}, {tif_meta['max']:.2f}] | CRS: {tif_meta['crs']}")
