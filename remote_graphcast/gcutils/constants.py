AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID' 
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_BUCKET = 'AWS_BUCKET'
CDS_URL = 'CDS_URL'
CDS_KEY = 'CDS_KEY'
FORCAST_LIST = 'GRAPHCAST_FORCAST_LIST'
CAST_ID = 'CAST_ID'
RUNPOD_KEY = "RUNPOD_KEY"


# from https://github.com/ecmwf-lab/ai-models-graphcast/blob/main/ai_models_graphcast/input.py 
CF_NAME_SFC = {
    "10u": "10m_u_component_of_wind",
    "10v": "10m_v_component_of_wind",
    "2t": "2m_temperature",
    "lsm": "land_sea_mask",
    "msl": "mean_sea_level_pressure",
    "tp": "total_precipitation_6hr",
    "z": "geopotential_at_surface",
}