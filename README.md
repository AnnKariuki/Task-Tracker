
# TASK TRACKER CLI APP

## Description
This is a simple lightweight command-line-interface(CLI) project used to track and manage your tasks.
It allows you to add, update, delete and list all your tasks all from your command line.

## Features
- **Add a Task** -> Create tasks with descriptions. Each task gets a unique ID and a default `todo` status.
- **Update a Task** -> Modify the description or status of a task.
- **Mark as In-Progress** ->  change a task’s status to `in-progress`.
- **Mark as Done** -> change a task’s status to `done`.
- **Delete a Task** -> Remove tasks by their ID.
- **List Tasks** -> Display all tasks or filter them by:
  - **status**: `todo`, `in-progress`, `done`, or `all`

## Usage
- add                 To add a task run: program_name add task_description
- update              To update a task run: program_name update task_id updated_description
- delete              To delete a task run: program_name delete task_id
- mark-in-progress    To mark a task as in progress run: program_name mark-in-progress task_id
- mark-done           To mark a task as done run: program_name mark-done task_id
- list                To list tasks run: program_name list [status]

BONUS - **Run any command with -h for more information e.g. 'Taskly list -h'**

## ⚡ Installation

You can install Taskly directly from GitHub:

```bash
git clone git@github.com:AnnKariuki/Task-Tracker.git
```