#!/usr/local/bin/python3
import argparse
import json
import datetime
import uuid
from pathlib import Path
import sys

# def initial_databse_setup(base_func):
#     def enhanced_func():
#         initial_data = []
#         try:
#             with open("database.json", "r+") as file:
#                 contents = file.read()
#                 if not contents:
#                     file.write(json.dumps(initial_data))
#         except IOError as e:
#             print(f"File write failed: {e}")
#         base_func()
#     return enhanced_func



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


def add_task(description):
    # task, time created, time updated, status
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    task_id = str(uuid.uuid4())
    task = {
        "id":task_id,
        "description": description,
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

# @initial_databse_setup
def main() -> None:
    parser = argparse.ArgumentParser("Welcome to taskly. Your one stop shop to track and manage your tasks")
    parser.add_argument("add", help="use 'add' keyword to add a task")
    parser.add_argument("description", help="describe your task")
    args = parser.parse_args()
    if args.add != "add":
        raise ValueError("the command to add a task is add")
    add_task(args.description)

main()