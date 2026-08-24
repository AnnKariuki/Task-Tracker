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

    @patch("task.is_database_empty")
    @patch('task.current_timestamp')
    @patch('task.load_database')
    @patch('task.save_database')
    def test_update_task(self, mock_save_database, mock_load_database, mock_current_time, mock_database_empty):
        mock_database_empty.return_value = False
        mock_current_time.return_value = "2026-08-23 20:08:35"
        args = argparse.Namespace(updated_description='buy rolls royce',task_id="1")
        mock_load_database.return_value = [
            {
                "id": "1",
                "description": "buy a company",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-22 14:46:17",
                "status": "todo"
            },
        ]
        task.update_task(args)
        mock_save_database.assert_called_once()
        mock_save_database.assert_called_with([
            {
                "id": "1",
                "description": "buy rolls royce",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-23 20:08:35",
                "status": "todo"
            }
        ])

    @patch("task.is_database_empty")
    @patch('task.current_timestamp')
    @patch('task.load_database')
    @patch('task.save_database')
    def test_delete_task(self, mock_save_database, mock_load_database, mock_current_time, mock_database_empty):
        mock_database_empty.return_value = False
        mock_current_time.return_value = "2026-08-23 20:08:35"
        args = argparse.Namespace(task_id="1")
        mock_load_database.return_value = [
            {
                "id": "1",
                "description": "buy a company",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-22 14:46:17",
                "status": "todo"
            },
        ]
        task.delete_task(args)
        mock_save_database.assert_called_once()
        mock_save_database.assert_called_with([])

    @patch('task.current_timestamp')
    @patch('task.load_database')
    @patch('task.save_database')
    def test_update_task_status(self, mock_save_database, mock_load_database, mock_current_time):

        mock_current_time.return_value = "2026-08-23 20:08:35"
        mock_load_database.return_value = [
            {
                "id": "1",
                "description": "buy a company",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-22 14:46:17",
                "status": "todo"
            },
        ]
        task.update_status("done", "1")
        mock_save_database.assert_called_once()
        mock_save_database.assert_called_with([
            {
                "id": "1",
                "description": "buy a company",
                "createdAt": "2026-08-22 14:46:17",
                "updatedAt": "2026-08-23 20:08:35",
                "status": "done"
            },
        ])

    @patch("task.is_database_empty")
    @patch("task.update_status")
    def test_mark_task_done(self, mock_update_status, mock_database_empty):
        mock_database_empty.return_value = False
        args = argparse.Namespace(task_id="1")
        task.mark_task_done(args)
        mock_update_status.assert_called_once_with(
            "done",
            "1"
        )

    @patch("task.is_database_empty")
    @patch("task.update_status")
    def test_mark_task_in_progress(self, mock_update_status, mock_database_empty):
        mock_database_empty.return_value = False
        args = argparse.Namespace(task_id="1")
        task.mark_task_in_progress(args)
        mock_update_status.assert_called_once_with(
            "in-progress",
            "1"
        )

    @patch("task.print")
    @patch("task.load_database")
    @patch("task.is_database_empty")
    def test_list_all_tasks(
        self,
        mock_is_database_empty,
        mock_load_database,
        mock_print,
    ):
        mock_is_database_empty.return_value = False

        mock_load_database.return_value = [
            {
                "id": "1",
                "description": "Buy groceries",
                "createdAt": "2026-08-23 10:00:00",
                "updatedAt": "2026-08-23 10:00:00",
                "status": "todo",
            }
        ]

        args = argparse.Namespace(
            status=None
        )

        task.list_tasks(args)

        mock_print.assert_any_call("ID: 1")
        mock_print.assert_any_call("description: Buy groceries")
        mock_print.assert_any_call("created at: 2026-08-23 10:00:00")
        mock_print.assert_any_call("updated at: 2026-08-23 10:00:00")
        mock_print.assert_any_call("status: todo")

    @patch("task.print")
    @patch("task.load_database")
    @patch("task.is_database_empty")
    def test_list_done_tasks(
        self,
        mock_is_database_empty,
        mock_load_database,
        mock_print,
    ):
        mock_is_database_empty.return_value = False

        mock_load_database.return_value = [
            {
                "id": "1",
                "description": "Buy groceries",
                "createdAt": "2026-08-23 10:00:00",
                "updatedAt": "2026-08-23 10:00:00",
                "status": "todo",
            },
            {
                "id": "2",
                "description": "Clean room",
                "createdAt": "2026-08-23 10:00:00",
                "updatedAt": "2026-08-23 10:00:00",
                "status": "done",
            },
        ]

        args = argparse.Namespace(
            status="done"
        )

        task.list_tasks(args)

        mock_print.assert_any_call("ID: 2")
        mock_print.assert_any_call("description: Clean room")
        mock_print.assert_any_call("status: done")
 

if __name__ == '__main__':
    unittest.main()