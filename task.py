#!/usr/local/bin/python3
import argparse
import json
import datetime
from pathlib import Path
import sys

def highest_id() -> int:
    data = load_database()
    max_id = 0
    for task in data:
        max_id = max(int(task["id"]), max_id)
    return max_id

def populate_database() -> None:
    initial_data = []
    try:
        with open("database.json", "w") as file:
            file.write(json.dumps(initial_data))
    except IOError as e:
        print(f"Error while initially populating the database file: {e}")
        sys.exit(1)


def is_database_empty() -> bool:
    database = Path("./database.json")
    if not database.exists():
        return True
    try:
        with open("database.json", "r") as file:
            contents = file.read()
            if not contents or contents.isspace():
                return True
            elif len(json.loads(contents)) == 0:
                return True
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while handling the empty database file: {e}")
        sys.exit(1)
    return False


def add_task(args) -> None:
    if is_database_empty():
        populate_database()
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    task_id = str(highest_id()+ 1)
    task = {
        "id":task_id,
        "description": args.new_description,
        "createdAt": dt_str,
        "updatedAt": dt_str,
        "status": "todo"
    }
    data = load_database()
    if not isinstance(data, list):
        data = []
    data.append(task)
    save_database(data)
    print(f"Task added successfully (ID:{task_id})")

def update_task(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    data = load_database()
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    updated = False
    for task in data:
        if task["id"] == args.task_id:
            task["description"] = args.updated_description
            task["updatedAt"] = dt_str
            updated = True
            updated_task = task
            break
    if not updated:
        print(f"No task found with ID '{args.task_id}'")
        return
    save_database(data)
    print(f"updated: task id [{updated_task['id']}], new description [{updated_task['description']}], status:[{updated_task['status']}]")
     

def delete_task(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    data = load_database()
    deleted = False
    for task in data:
        if task["id"] == args.task_id:
            data.remove(task)
            deleted = True
            deleted_task = task
            break
    if not deleted:
        print(f"There is no item with id {args.task_id} in our system")
        return
    save_database(data)
    print(f"deleted: task id [{deleted_task['id']}], description [{deleted_task['description']}], status:[{deleted_task['status']}]")

def mark_task_in_progress(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    update_status("in-progress",args.task_id)

def mark_task_done(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    update_status("done",args.task_id)

def update_status(new_status, task_id):
    data = load_database()
    found = False
    for task in data:
        if task["id"] == task_id:
            if task["status"] == new_status:
                print(f"your task is already marked as {new_status}")
                return
            else:
                task["status"] = new_status
                dt = datetime.datetime.now()
                dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                task["updatedAt"] = dt_str
                updated_task = task
                found = True 
            break
    if not found:
        print(f"no task with id {task_id}")
        return          
    save_database(data)
    print(f"updated status: task id [{updated_task['id']}], description [{updated_task['description']}], new status:[{updated_task['status']}]")

def load_database() -> list:
    try:
        with open("database.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
        print(f"had trouble performing task: {e}")
        sys.exit(1)

def save_database(data):
    try:
        with open("database.json", "w") as file:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except FileNotFoundError as e:
        print(f"had trouble performing task: {e}")
        sys.exit(1)
        
def list_tasks(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    data = load_database()
    if not args.status:
        full_list = data
    else:
        full_list = [task for task in data if task["status"] == args.status]
    if not full_list:
        print(f"No task with status {args.status}")
    else:
        for task in full_list:
            print(f"ID: {task['id']}")
            print(f"description: {task['description']}")
            print(f"created at: {task['createdAt']}")
            print(f"updated at: {task['updatedAt']}")
            print(f"status: {task['status']}")
            print()

def main() -> None:
    parser = argparse.ArgumentParser(prog="Taskly", description="Welcome to taskly. Your one stop shop to track and manage your tasks", epilog="Thanks for visiting")
    subparsers = parser.add_subparsers(title="What you can do in taskly",  description="Run any command with -h for more information, e.g. 'Taskly list -h'", required=True)

    add_subparser = subparsers.add_parser('add', help='To add a task run: program_name add task_description')
    add_subparser.add_argument('new_description')
    add_subparser.set_defaults(func=add_task)

    update_subparser = subparsers.add_parser('update', help='To update a task run: program_name update task_id updated_description')
    update_subparser.add_argument('task_id')
    update_subparser.add_argument('updated_description')
    update_subparser.set_defaults(func=update_task)

    delete_subparser = subparsers.add_parser('delete', help='To delete a task run: program_name delete task_id')
    delete_subparser.add_argument('task_id')
    delete_subparser.set_defaults(func=delete_task)

    mark_in_progress_subparser = subparsers.add_parser('mark-in-progress', help='To mark a task as in progress run: program_name mark-in-progress task_id')
    mark_in_progress_subparser.add_argument('task_id')
    mark_in_progress_subparser.set_defaults(func=mark_task_in_progress)

    mark_done_subparser = subparsers.add_parser('mark-done', help='To mark a task as done run: program_name mark-done task_id')
    mark_done_subparser.add_argument('task_id')
    mark_done_subparser.set_defaults(func=mark_task_done)

    list_subparser = subparsers.add_parser( 'list', help='To list tasks run: program_name list [status]')
    list_subparser.add_argument('status', nargs='?', choices=['todo', 'in-progress', 'done'],  help="Filter tasks by status: todo, in-progress, or done")
    list_subparser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    args.func(args)


main()