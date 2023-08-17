"""
Task Manager Program by Vaidas Razgaitis
"""
import argparse


class Tasks:
    """A list of `Task` objects."""

    def __init__(self, name, priority=1, due=None):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = []

        # your code here
        self.name = name
        self.priority = priority
        self.due = due

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


# parser = argparse.ArgumentParser(
#     description='Create a task list. Tasks can be added, deleted, listed, and marked as complete.')

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

task_1 = Tasks(name=args.name,
               priority=args.priority,
               due=args.due)

print(f'task name: {task_1.name}')
print(f'task due date: {task_1.due}')
print(f'task priority: {task_1.priority}')
