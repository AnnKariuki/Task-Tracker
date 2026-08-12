#!/usr/local/bin/python3
import argparse
import json
import datetime
def addTask(description):
    # task, time created, time updated, status
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    task = {
        "description": description,
        "time_created": dt_str,
        "time_updated": dt_str,
        "status": "todo"
    }
    try:
        with open("database.json", "a") as file:
            file.write(json.dumps(task))
    except IOError as e:
        print(f"File write failed: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Welcome to taskly. Your onestop shop to track and manage your tasks")
    parser.add_argument("add", help="use 'add' keyword to add a task")
    parser.add_argument("description", help="describe your task")
    args = parser.parse_args()
    addTask(args.description)
