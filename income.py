
""" 
The Relationship Between Food Access in New York State in 2019
Final Data Analysis Project
Professor Wilcoxen
Author: Kerri Riley 
Date: 3/26/2026  

"""

# Import modules
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt 


# Heat map of food access across counties in New York State on QGIS
# Put "STATEFP" = '36'in query builder to narrow it down to NYS


# Food desert if LILATracts_1And10, High % of low-income + low-access tracts
# municipalitie ("Places in US Census Shapefile
# find out their methodology and look at it in a finer level

 



# Load county shapefile
counties = gpd.read_file("tl_2019_us_county.zip")

# Keep only New York
ny_counties = counties[counties["STATEFP"] == "36"].copy()
ny_counties["GEOID"] = ny_counties["GEOID"].astype(str).str.zfill(5)

 

# Load food access data
food = pd.read_csv("Food_Access.csv")

# Clean + keep NY only
food["CensusTract"] = food["CensusTract"].astype(str).str.zfill(11)
food = food[food["CensusTract"].str.startswith("36")]

# Create county GEOID
food["GEOID"] = food["CensusTract"].str[:5]

# Aggregate to county
food_county = food.groupby("GEOID", as_index=False).agg({
    "MedianFamilyIncome": "mean",
    "LILATracts_1And10": "mean"
})


# Merge
ny_merged = ny_counties.merge(food_county, on="GEOID", how="left")

# Drop missing
ny_merged = ny_merged.dropna(subset=["MedianFamilyIncome", "LILATracts_1And10"])


# SIMPLE food desert measure 
# Higher = worse access
ny_merged["food_desert_score"] = (
    ny_merged["LILATracts_1And10"] / ny_merged["MedianFamilyIncome"]
)



# Scatter Plot Showing Income and Food Access
plt.figure(figsize=(8, 5))

plt.scatter(
    ny_merged["MedianFamilyIncome"],
    ny_merged["LILATracts_1And10"],
    alpha=0.6
)

plt.xlabel("Median Family Income")
plt.ylabel("Low Access Tracts (avg)")
plt.title("NY Counties: Income vs Food Access")
plt.show()



# Export for QGIS
ny_merged.to_file("ny_food_desert.gpkg", driver="GPKG")