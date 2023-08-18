"""
Task Manager Program by Vaidas Razgaitis
"""
import argparse
import datetime
import sys
import pickle
import pprint


class Task:
    """Representation of a task"""
    # TODO: unique identifier when a task has been instantiated
    #   -use a generator for this?

    def __init__(self, name, priority, unique_id, completed=None, due=None):
        self.created = datetime.datetime.now()
        self._parse_date_string()
        self.completed = completed
        self.name = name.lower()
        self.priority = priority
        self.due = due
        self._cleanup_due_format()
        self.id = unique_id

    def _parse_date_string(self):
        """
        Parse the date string into the desired format:
        <Mon Mar  5 12:10:08 CST 2018>
        
        Data comes in from datetime.now() as
        year, month, day, hour, minute, second, and microsecond
        <YYYY-MM-DD hh:mm:ss. ffffff>
        """
        # self.time_created = self.created.time()
        self.created = self.created.strftime("%a %b  %d %I:%M:%S CST %Y")
    
    def _complete_task(self):
        """
        Get current time when a task has been marked as complete.
        
        Parse the date object into the desired format:
        <Mon Mar  5 12:10:08 CST 2018>
        """
        self.completed = datetime.datetime.now()
        self.completed = self.completed.strftime("%a %b  %d %I:%M:%S CST %Y")
    
    def _cleanup_due_format(self):
        """
        Cleanup date to consistent format for clean printing
        
        For example, converts
        9/3/2023 to 09/03/2023
        """
        date_components = self.due.split('/')
        if len(date_components) != 3:
            raise ValueError("Invalid date format")
        month, day, year = date_components
        # infil zeros where needed
        formatted_month = month.zfill(2)
        formatted_day = day.zfill(2)
        self.due = f'{formatted_month}/{formatted_day}/{year}'


class Tasks:
    """A list of `Task` objects."""

    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        self.tasks = []

        try:
            with open('.todo.pickle', 'rb') as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            # pickling of objects list is done just before exiting the program
            pass

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open('.todo.pickle', 'wb') as file:
            pickle.dump(self.tasks, file)

    def list(self):
        """
        Console print a sorted list of outstanding tasks.
        """
        # TODO: separate sorting method, using higher order lambda fn on:
        #       -priority to having a due date
        #       -only print NON-DONE items
        #       -whole list sorted by priority otherwise
        #       -can just thru twice, once sorting due dates present
        print('\nID   Age  Due Date    Priority   Task')
        print('--   ---  ----------  --------   ----')
        for task in self.tasks:
            print(f'{task.id}    Age  {task.due}  {task.priority}          {task.name}')
        print('\n')
        
    def report(self):
        print('\nID   Age  Due Date    Priority   Task                Created                       Completed')
        print('--   ---  ----------  --------   ----                ---------------------------   -------------------------')
        for task in self.tasks:
            print(f'{task.id}    Age  {task.due}  {task.priority}          {task.name}            {task.created}          {"-" if not task.completed else task.completed}')
        print('\n')
        
    def done(self, completed_task_id):
        """
        Updates the "completed" attribute for a completed task object
        """
        # Pop a completed task out of the tasklist
        finished_task = [self.tasks.pop(index) for index, task in enumerate(self.tasks) if task.id == completed_task_id][0]
        finished_task._complete_task()
        print("Completed task", finished_task.id)
        self.tasks.append(finished_task)
        
    def query(self):
        pass

    def add(self, new_task):
        """Add a task to the tasklist and console print the ID#"""
        self.tasks.append(new_task)
        print("Created task", new_task.id)

def main():
    # Create parser
    parser = argparse.ArgumentParser(description='update your TODO list')
    
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
    # print('Add:', args.add)
    # print('Due:', args.due)
    # print('priority:', args.priority)
    # print('Query:', args.query)
    # print('List:', args.list)
    # print('Done:', args.done)
    # print('Delete:', args.delete)
    # print('Report:', args.report)

    # unpickle existing tasklist if needed
    tasklist = Tasks()
    
    if args.add:
        # Instantiate a new task object
        new_task = Task(name=args.add,
                        priority=args.priority,
                        due=args.due,
                        unique_id=len(tasklist.tasks) + 1)
        # add new task to the existing tasklist
        tasklist.add(new_task)
    
    elif args.query:
        print('QUERY functionality to be coded.')
    elif args.list:
        tasklist.list()
    elif args.done:
        tasklist.done(args.done)
    elif args.delete:
        print('delete program to be coded.')
    elif args.report:
        tasklist.report()
    
    # pickle tasklist and exit
    tasklist.pickle_tasks()
    exit()

if __name__ == "__main__":
    main()
    
