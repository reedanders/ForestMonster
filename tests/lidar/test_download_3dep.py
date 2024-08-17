import unittest
from unittest.mock import patch, MagicMock
from data_processing.lidar.download_3dep import download_3dep_lidar

class TestDownload3DEP(unittest.TestCase):

    @patch('data_processing.lidar.download_3dep.boto3.client')
    def test_download_3dep_lidar(self, mock_boto_client):
        # Mock the S3 client and response
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        # Call the function
        download_3dep_lidar('test_region.geojson', 'output_dir')

        # Assert that the correct calls were made to the S3 client
        mock_s3.download_file.assert_called()

if __name__ == '__main__':
    unittest.main()
