"""
Task Manager Program by Vaidas Razgaitis
"""
import argparse
import datetime
import sys
import pickle


class Task:
    """Representation of a task"""
    # TODO: unique identifier when a task has been instantiated
    #   -use a generator for this?

    def __init__(self, name, priority, unique_id, completed=None, due=None):
        self.created = datetime.datetime.now()
        self._parse_date_string()
        self.completed = completed
        self.name = name
        self.priority = priority
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

        try:
            with open('.todo.pickle', 'rb') as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            # self.pickle_tasks()
            pass

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open('.todo.pickle', 'wb') as file:
            pickle.dump(self.tasks, file)

    def list(self):
        pass

    def report(self):
        pass

    def done(self):
        pass

    def query(self):
        pass

    def add(self, task_info):
        """Add a task to the tasklist and console print the ID#"""
        self.tasks.append(task_info)
        print("Created task", task_info.id)


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

    # Create parser
    parser = argparse.ArgumentParser(description='update your TODO list')
    tasklist = Tasks()
    
    # Add necessary arguements
    parser.add_argument('--add', type=str, required=False, help='a string describing your task to add')
    parser.add_argument('--due', type=str, required=False, help='date the task must be completed by, in MM/dd/YYYY format')
    parser.add_argument('--priority', type=int, required=False, default=1, help='task priority; default is 1')
    parser.add_argument('--query', type=str, required=False, nargs="+", help='a string that will be searched among existing tasks')
    parser.add_argument('--list', action='store_true', required=False, help='list all remaining tasks to be completed')
    parser.add_argument('--done', type=int, required=False, help='<ID#> of a task that has been completed')
    parser.add_argument('--delete', type=int, required=False, help='<ID#> of a task to be removed from the list')
    parser.add_argument('--report', action='store_true', required=False, help='list a full report of completed and remaining tasks')
    
    # Parse arguements    
    args = parser.parse_args()
    
    # print results
    print('Add:', args.add)
    print('Due:', args.due)
    print('priority:', args.priority)
    print('Query:', args.query)
    print('List:', args.list)
    print('Done:', args.done)
    print('Delete:', args.delete)
    print('Report:', args.report)

    if user_action == '--add':
        # Instantiate a new task object
        new_task = Task(name=args.add,
                        priority=args.priority,
                        due=args.due,
                        unique_id=len(tasklist.tasks) + 1)

        tasklist.add(new_task)
        tasklist.pickle_tasks()
        exit()
