import unittest
from unittest.mock import patch, MagicMock
import h5py
import os
from data_processing.lidar.process_lidar import process_lidar_data

class TestProcessLidar(unittest.TestCase):

    @patch('data_processing.lidar.process_lidar.Pipeline')
    def test_process_lidar_data(self, mock_pdal_pipeline):
        # Mock the PDAL pipeline
        mock_pipeline = MagicMock()
        mock_pdal_pipeline.return_value = mock_pipeline
        mock_pipeline.execute.return_value = True

        # Create a mock LAS file
        las_file = 'test_data.las'
        output_dir = 'test_output'

        # Run the function
        process_lidar_data(las_file, output_dir)

        # Verify that PDAL pipeline was executed
        mock_pipeline.execute.assert_called_once()

        # Check if HDF5 file is created (you may want to mock h5py as well)
        output_file = os.path.join(output_dir, 'test_data.h5')
        self.assertTrue(os.path.exists(output_file))

        # Clean up (remove mock files)
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
