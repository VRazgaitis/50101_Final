"""
Task Manager Program by Vaidas Razgaitis
"""
import argparse
import datetime
import sys


class Task:
    """Representation of a task"""
    # TODO: unique identifier when a task has been instantiated
    #   -use a generator for this?

    def __init__(self, name, priority, unique_id, completed=None, due=None):
        self.created = datetime.datetime.now()
        self.completed = completed
        self._parse_date_string()
        self.name = name
        self.priority = priority if priority else 1
        self.due = due
        self.id = unique_id

    def _parse_date_string(self):
        """
        Parse the date string into the desired format:
        <Mon Mar  5 12:10:08 CST 2018>
        """
        self.time_created = self.created.time()
        self.created = self.created.strftime("%a %b  %d %I:%M:%S CST %Y")


class Tasks:
    """A list of `Task` objects."""

    def __init__(self, task_info=None):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = []
        # self.task_data = task_info

    def pickle_tasks(self):
        """Picle your task list to a file"""
        # your code here

    def list(self):
        pass

    def report(self):
        pass

    def done(self):
        pass

    def query(self):
        pass

    def add(self, task_info):
        self.tasks.append(task_info)


def command_valid(user_action):
    """Ensure that the user has chosen a valid action verb"""
    # Only 6 approved verbs
    action_options = ['--add',
                      '--delete',
                      '--list',
                      '--report',
                      '--query',
                      '--done']

    if user_action not in action_options:
        print('There was an error in choosing TODO list actions. Run "todo -h" for usage instructions.')
        return False
    else:
        return True


if __name__ == "__main__":
    # get the user's action verb
    user_action = (sys.argv[1])

    if command_valid(user_action):
        # Create parser
        parser = argparse.ArgumentParser()
        tasklist = Tasks()

        if user_action == '--add':
            # Add name argument
            parser.add_argument('--add', type=str, required=False)
            # Add due date argument
            parser.add_argument('--due', type=str, required=False)
            # Add priority argument
            parser.add_argument('--priority', type=str, required=False)
            args = parser.parse_args()

            # Instantiate a task object
            new_task = Task(name=args.add,
                            priority=args.priority,
                            due=args.due,
                            unique_id=len(tasklist.tasks) + 1)

            tasklist.add(new_task)
