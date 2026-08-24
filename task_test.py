#!/usr/local/bin/python3
import unittest
import task
from unittest.mock import patch
import argparse
class TestTaskTrackerMethods(unittest.TestCase):
    @patch("task.is_database_empty")
    @patch('task.current_timestamp')
    @patch('task.highest_id')
    @patch('task.load_database')
    @patch('task.save_database')
    def test_add_task(self, mock_save_database, mock_load_database, mock_highest_id, mock_current_time, mock_database_empty):
        mock_database_empty.return_value = False
        mock_current_time.return_value = "2026-08-22 14:46:17"
        mock_highest_id.return_value = 1
        args = argparse.Namespace(new_description='visit rolls royce dealership')
        mock_load_database.return_value = [
            {
                "id": "1",
                "description": "buy a company",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-22 14:46:17",
                "status": "todo"
            },
        ]
        task.add_task(args)
        # we have this after we call add task because it is only called after the mthod runs
        mock_save_database.assert_called_once()
        mock_save_database.assert_called_with([
            {
                "id": "1",
                "description": "buy a company",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-22 14:46:17",
                "status": "todo"
            },
            {
                "id": "2",
                "description": "visit rolls royce dealership",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-22 14:46:17",
                "status": "todo"
            }
        ])

if __name__ == '__main__':
    unittest.main()