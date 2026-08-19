#!/usr/local/bin/python3
import argparse
import json
import datetime
from pathlib import Path
import sys

def get_db_size()-> int:
    try:
        with open("database.json","r") as file:
            contents = json.loads(file.read())
            db_size = len(contents)
    except IOError as e:
        print(f"having trouble getting length of file: {e}")
        sys.exit(1)
    return db_size

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
    task_id = str(get_db_size()+ 1)
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
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while adding task to the database file: {e}")
        sys.exit(1)
    print(F"Task added successfully (ID:{task_id})")

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
            if updated == False:
                print("Task does not exist in database")
                sys.exit(0)
            file.seek(0)
            json.dump(data, file, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while updating task in the database file: {e}")
        sys.exit(1)

        
def main() -> None:
    parser = argparse.ArgumentParser(prog="Taskly", description="Welcome to taskly. Your one stop shop to track and manage your tasks", epilog="Thanks for visiting")
    subparsers = parser.add_subparsers(title="What you can do in taskly")

    add_subparser = subparsers.add_parser('add', help='To add a task run: program_name add task_description')
    add_subparser.add_argument('new_description')
    add_subparser.set_defaults(func=add_task)

    update_subparser = subparsers.add_parser('update', help='To update a task run: program_name update task_id updated_description')
    update_subparser.add_argument('task_id')
    update_subparser.add_argument('updated_description')
    update_subparser.set_defaults(func=update_task)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)


main()