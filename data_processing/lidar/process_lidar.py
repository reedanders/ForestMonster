import os
import numpy as np
import pdal
import h5py
from pathlib import Path

def read_lidar(las_file):
    """
    Reads the LAS file and converts it into a NumPy array.
    
    Parameters:
    las_file (str): Path to the LAS file.

    Returns:
    np.ndarray: Array containing the point cloud data.
    """
    pipeline = pdal.Pipeline(f"""
    {{
        "pipeline": [
            "{las_file}",
            {{
                "type": "filters.range",
                "limits": "Classification![7:7]"
            }},
            {{
                "type": "filters.hag"
            }},
            {{
                "type": "filters.normal",
                "knn": 8
            }},
            {{
                "type": "filters.ferry",
                "dimensions": "X=1.0:X, Y=1.0:Y, Z=1.0:Z"
            }}
        ]
    }}
    """)
    
    pipeline.execute()
    point_cloud = pipeline.arrays[0]
    
    return point_cloud

def convert_to_pointcept_format(point_cloud, output_file):
    """
    Converts the processed point cloud data to a format compatible with Pointcept.
    
    Parameters:
    point_cloud (np.ndarray): The processed point cloud data.
    output_file (str): Path to the output HDF5 file.
    """
    # Extract necessary features
    x = point_cloud['X']
    y = point_cloud['Y']
    z = point_cloud['Z']
    intensity = point_cloud['Intensity']
    classification = point_cloud['Classification']
    
    # Prepare data in the required format
    points = np.stack([x, y, z, intensity, classification], axis=-1)
    
    # Write to HDF5
    with h5py.File(output_file, 'w') as f:
        f.create_dataset("point_cloud", data=points)

def process_lidar(las_dir, output_dir):
    """
    Processes all LAS files in a directory and converts them to Pointcept format.

    Parameters:
    las_dir (str): Directory containing the LAS files.
    output_dir (str): Directory to save the processed HDF5 files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for las_file in Path(las_dir).glob("*.las"):
        print(f"Processing {las_file}...")
        point_cloud = read_lidar(str(las_file))
        output_file = os.path.join(output_dir, las_file.stem + '.h5')
        convert_to_pointcept_format(point_cloud, output_file)
        print(f"Saved processed data to {output_file}")

if __name__ == "__main__":
    # Example usage
    las_dir = "lidar_data/"
    output_dir = "processed_lidar_data/"
    
    process_lidar(las_dir, output_dir)
