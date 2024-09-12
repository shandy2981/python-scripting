import unittest
from unittest.mock import patch
from cli_tool.commands.backup import take_rds_snapshot, copy_snapshot_to_s3

class TestRDSBackup(unittest.TestCase):

    @patch('boto3.client')
    def test_take_rds_snapshot(self, mock_boto_client):
        mock_rds = mock_boto_client.return_value
        mock_rds.create_db_snapshot.return_value = {
            'DBSnapshot': {'DBSnapshotIdentifier': 'test-snapshot-id'}
        }
        snapshot_id = take_rds_snapshot('test-instance-id')
        self.assertEqual(snapshot_id, 'test-snapshot-id')

    @patch('boto3.client')
    def test_copy_snapshot_to_s3(self, mock_boto_client):
        mock_s3 = mock_boto_client.return_value
        copy_snapshot_to_s3('test-snapshot-id', 'test-bucket')
        mock_s3.upload_file.assert_called_with('test-snapshot-id', 'test-bucket', 'test-snapshot-id.rds')

if __name__ == '__main__':
    unittest.main()