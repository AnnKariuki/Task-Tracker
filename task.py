#!/usr/local/bin/python3
import argparse
import json
import datetime
from pathlib import Path
import sys

def highest_id() -> int:
    try:
        with open("database.json","r") as file:
            contents = json.loads(file.read())
            max_id = 0
            for task in contents:
                max_id = max(int(task["id"]), max_id)
    except (IOError, json.JSONDecodeError) as e:
        print(f"having trouble getting the max id assigned to one of your tasks: {e}")
        sys.exit(1)
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
    except IOError as e:
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

    try:
        with open("database.json", "r+") as file:
            data = json.loads(file.read())
            if not isinstance(data, list):
                data = []
            data.append(task)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while adding task to the database file: {e}")
        sys.exit(1)
    print(f"Task added successfully (ID:{task_id})")

def update_task(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    try:
        with open('database.json', 'r+') as file:
            data = json.loads(file.read())
            dt = datetime.datetime.now()
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            updated = False
            for dictionary in data:
                if dictionary["id"] == args.task_id:
                    dictionary["description"] = args.updated_description
                    dictionary["updatedAt"] = dt_str
                    updated = True
                    break
            if not updated:
                print("Task does not exist in database")
                return
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while updating task in the database: {e}")
        sys.exit(1)

def delete_task(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    try:
        with open('database.json', "r+") as file:
            data = json.load(file)
            deleted = False
            for task in data:
                if task["id"] == args.task_id:
                    data.remove(task)
                    deleted = True
                    break
            if not deleted:
                print(f"There is no item with id {args.task_id} in our system")
                return
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while deleting your task in database: {e}")
        sys.exit(1)

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
    try:
        with open('database.json', "r+") as file:
            data = json.load(file)
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
                        found = True 
                    break
            if not found:
                print(f"no task with id {task_id}")
                return          
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except (IOError, json.JSONDecodeError) as e:
        print(f"Had trouble updating the status of your task: {e}")    
        sys.exit(1)

def list_tasks(args) -> None:
    if is_database_empty():
        print('No tasks in database')
        return
    try:
        with open("database.json", "r") as file:
            data = json.load(file)
            if not args.status:
                full_list = data
            else:
                full_list = [task for task in data if task["status"] == args.status]
            if not full_list:
                print(f"No task with status {args.status}")
            else:
                # print(*full_list, sep='\n')
                # pretty print
                for task in full_list:
                    print(f"ID: {task['id']}")
                    print(f"description: {task['description']}")
                    print(f"created at: {task['createdAt']}")
                    print(f"updated at: {task['updatedAt']}")
                    print(f"status: {task['status']}")
                    print("\n")

    except (IOError, json.JSONDecodeError) as e:
        print(f"error listing your tasks: {e}")

def main() -> None:
    # 1. Create top-level parser
    parser = argparse.ArgumentParser(prog="Taskly", description="Welcome to taskly. Your one stop shop to track and manage your tasks", epilog="Thanks for visiting")
    # 2. Add subparsers container. subcommand must be provided
    subparsers = parser.add_subparsers(title="What you can do in taskly",  description="Run any command with -h for more information, e.g. 'Taskly list -h'", required=True)

    # 3. Define the 'add' subcommand
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

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)


main()