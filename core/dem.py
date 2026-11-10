import os 
import pandas as pd
import geopandas as gpd

"""
Randolph Glacier Inventory (RGI) v7.0 is a global dataset of glacier outlines and attributes, released in September 2023 (Maussion et al., 2022). 
In this module, we are particularly interested in collecting the CenLat, CenLon and glims_id from the user-specified glacier. 
This shapefile is used to crop the Digital Elevation Model (DEM) because performing the vectorial shading algorithm on a whole DEM would be too computationally expensive. 
"""

def load_attributes(inputs):
    """
    Loads RGI2000 v7.0 Region 19 attributes for the user-specified glacier; this requires the 'RGI2000-v7.0-G-06_iceland-attributes.csv' file found in the data folder of the repository. 
    These attributes include CenLat, CenLon and glims_id used for getting the shapefile.
    
    Parameters
    ----------
    inputs : dict
        ['input_dir'] : str
            Root directory where all the data is stored, including the 'RGI2000-v7.0-G-06_iceland-attributes.csv' file.
        ['name'] : str
            The name of the glacier that requires attributes loading.
    Returns
    ----------
    attributes.iloc[0] : pandas.core.series.Series
        A one-dimensional array containing glacier attributes. 

    Examples
    ----------
    inputs = {}
    inputs['input_dir'] = '/Users/billy/Desktop/igs/model/data/'
    inputs['name'] = 'Breidamerkurjoekull'
    load_attributes(inputs)
  
    """ 
    
    attributes_path = os.path.join(inputs['input_dir'],'RGI2000-v7-2/RGI2000-v7.0-G-06_iceland-attributes.csv')
    regional_attributes = pd.read_csv(attributes_path).dropna()
    attributes = regional_attributes[regional_attributes['glac_name'].str.contains(inputs['name'])]

    return attributes.iloc[0]

def load_shapefile(inputs):
    """
    Loads RGI2000 v7.0 Region 19 shapefile for the user-specified glacier, filtering through Global Land Ice Measurements from Space IDs (glims_id). 
    
    Parameters
    ----------
    inputs : dict
        ['input_dir'] : str
            Root directory where all the data is stored, including the 'RGI2000-v7.0-G-06_iceland.shp' file.
        ['name'] : str 
            The name of the glacier that requires attributes loading.

    Returns
    ----------
    shapefile : geopandas.geodataframe.GeoDataFrame
        Extended pandas.DataFrame storing geometry of glacier as a polygon 

    Examples
    ----------
    # Importing matplotlib.pyplot 
    import matplotlib.pyplot as plt
    # Define your inputs
    inputs = {}
    inputs['input_dir'] = '/Users/billy/Desktop/igs/model/data/'
    inputs['name'] = 'Breidamerkurjoekull'
    # Load the shapefile 
    shapefile = load_shapefile(inputs)
    # Plotting the shapefile 
    geometry = shapefile['geometry']
    plt.plot(geometry)
  
    """ 
    
    shapefile_path = os.path.join(inputs['input_dir'],'RGI2000-v7-2/RGI2000-v7.0-G-06_iceland.shp')
    regional_shapefiles = gpd.read_file(shapefile_path)
    attributes = load_attributes(inputs)
    shapefile = regional_shapefiles[regional_shapefiles['glims_id'].isin([attributes['glims_id']])]

    return shapefile

"""
References
Maussion, F., Hock, R., Paul, F., Rastner, P., Raup, B., Zemp, M. and RGI Consortium, 2022, May. The Randolph glacier inventory (RGI) version 7. In EGU General Assembly Conference Abstracts (pp. EGU22-4484).
"""
