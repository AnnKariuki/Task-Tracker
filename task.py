#!/usr/local/bin/python3
import argparse
import json
import datetime
import uuid
from pathlib import Path
import sys

def populate_database():
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


def add_task(args):
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    task_id = str(uuid.uuid4())
    task = {
        "id":task_id,
        "description": args.new_description,
        "createdAt": dt_str,
        "updatedAt": dt_str,
        "status": "todo"
    }
    if is_database_empty():
        populate_database()

    try:
        with open("database.json", "r+") as file:
            data = json.loads(file.read())
            if not isinstance(data, list):
                data = []
            data.append(task)
            file.seek(0)
            json.dump(data, file, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error while handling the database file: {e}")
        sys.exit(1)
    print(F"Task added successfully (ID:{task_id} )")

def update_task(args):
    print(args.task_id)
    print(args.updated_description)

def main() -> None:
    parser = argparse.ArgumentParser(prog="Taskly", description="Welcome to taskly. Your one stop shop to track and manage your tasks", epilog="Thanks for visiting")
    subparsers = parser.add_subparsers(title="What you can do in taskly")

    add_subparser = subparsers.add_parser('add', help='To add a task run: program_name add task_description')
    add_subparser.add_argument('new_description')
    add_subparser.set_defaults(func=add_task)

    update_subparser = subparsers.add_parser('update', help='To update a task run: program_name task_id updated_description')
    update_subparser.add_argument('task_id')
    update_subparser.add_argument('updated_description')
    update_subparser.set_defaults(func=update_task)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)


main()