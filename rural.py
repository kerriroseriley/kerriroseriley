
"""
The Relationship Between Rural and Urban counties and Food Access in the United State in 2019
Final Data Analysis Project
Professor Wilcoxen
Author: Kerri Riley 
Date: 3/26/2026  
"""

# Import modules
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt 


rural = gpd.read_file("tl_2019_us_uac10.zip")

ny_rural = rural[rural["STATEFP"] == "36"].copy()
ny_rural["GEOID"] = ny_rural["GEOID"].astype(str).str.zfill(5)


