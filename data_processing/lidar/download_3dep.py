import os
import boto3
import subprocess
import json
from botocore import UNSIGNED
from botocore.client import Config

# AWS S3 settings
EPT_S3_BUCKET = "usgs-lidar-public"
EPT_S3_PREFIX = "ept/"
DOWNLOAD_DIR = "lidar_data/"

def download_lidar_tiles(geojson_file, output_dir=DOWNLOAD_DIR):
    """
    Download 3DEP LiDAR data in EPT format from S3 based on a given GeoJSON file.
    
    Parameters:
    geojson_file (str): Path to the GeoJSON file defining the area of interest.
    output_dir (str): Directory where the LiDAR data will be downloaded.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load GeoJSON to get the bounding box
    with open(geojson_file, 'r') as f:
        geojson = json.load(f)
    
    bbox = get_bbox_from_geojson(geojson)
    
    # Define S3 client (anonymous access)
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    # Define Entwine Point Tiles (EPT) location on S3
    ept_location = f"s3://{EPT_S3_BUCKET}/{EPT_S3_PREFIX}"
    
    # Use PDAL to fetch LiDAR data
    command = [
        "pdal", "pipeline",
        "--readers.ept.s3",
        "--writers.las.filename", os.path.join(output_dir, "output.las"),
        "--filters.crop.bounds", f"([{bbox[0]}, {bbox[2]}], [{bbox[1]}, {bbox[3]}])",
        "--readers.ept.filename", ept_location
    ]
    
    print(f"Running command: {' '.join(command)}")
    
    subprocess.run(command, check=True)

def get_bbox_from_geojson(geojson):
    """
    Extracts bounding box from a GeoJSON file.
    
    Parameters:
    geojson (dict): The loaded GeoJSON data.
    
    Returns:
    list: Bounding box in the format [min_lon, min_lat, max_lon, max_lat].
    """
    coords = geojson['features'][0]['geometry']['coordinates'][0]
    min_lon = min([coord[0] for coord in coords])
    max_lon = max([coord[0] for coord in coords])
    min_lat = min([coord[1] for coord in coords])
    max_lat = max([coord[1] for coord in coords])
    
    return [min_lon, min_lat, max_lon, max_lat]

if __name__ == "__main__":
    # Example usage:
    geojson_path = "path/to/your/area.geojson"
    download_lidar_tiles(geojson_path)
