"""
Task Manager Program by Vaidas Razgaitis
"""
import argparse
import datetime


class Task:
    """Representation of a task"""
    # TODO: unique identifier when a task has been instantiated
    #   -use a generator for this?

    def __init__(self, name, priority, completed=None, due=None):
        self.created = datetime.datetime.now()
        self.completed = completed
        self._parse_date_string()
        self.name = name
        self.priority = priority if priority else 1
        self.due = due

    def _parse_date_string(self):
        """
        Parse the date string into the desired format:
        <Mon Mar  5 12:10:08 CST 2018>
        """
        self.time_created = self.created.time()
        self.created = self.created.strftime("%a %b  %d %I:%M:%S CST %Y")


class Tasks:
    """A list of `Task` objects."""

    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = []

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

    def add(self):
        pass


# Create the parser
parser = argparse.ArgumentParser()

# Add name argument
parser.add_argument('--name', type=str, required=True)

# Add due date argument
parser.add_argument('--due', type=str, required=False)

# Add priority argument
parser.add_argument('--priority', type=str, required=False)

# Parse the argument
args = parser.parse_args()

task_1 = Task(name=args.name,
              priority=args.priority,
              due=args.due)

print(f'task name: {task_1.name}')
print(f'task due date: {task_1.due}')
print(f'task priority: {task_1.priority}')
print(f'task created: {task_1.created}')
