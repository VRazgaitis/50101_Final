"""
Task Manager Program by Vaidas Razgaitis

PROGRAM REQUIREMENTS:
---------------------
Take input arguments to:
-add/delete task 
-mark task as complete
-list remaining tasks
-search remaining tasks for keywords
-report all tasks (remaining AND complete)


PROGRAM SUMMARY
----------------
-Takes action verb input arguement
-Instantiates Tasks tasklist (reads pickle file containing tasklist, if it exists)
-Instantiates new Task objects or modifies existing ones
-Pickles modified Tasks list of Task objects into a binary file, <.todo.pickle>, in the pwd

Tabulate documentation:
https://pypi.org/project/tabulate/
"""
import argparse
import datetime
import pickle
from tabulate import tabulate
from functools import reduce


class Task:
    """Representation of a task"""
    def __init__(self, name, priority, unique_id, completed=None, due=None):
        self.created = self._get_time()
        self.completed = completed
        self.name = name.lower()
        self.priority = priority
        self.due = due
        if due is not None: self._cleanup_due_format()
        self.id = unique_id
        self.task_age = None

    def _get_time(self):
        """
        Get current time and parse string into the desired format:
        <Mon Mar  5 12:10:08 CST 2018>
        """
        # Format: <YYYY-MM-DD hh:mm:ss. ffffff>
        self.created_time_obj = datetime.datetime.now()
        current_time = datetime.datetime.now()
        return current_time.strftime("%a %b  %d %I:%M:%S CST %Y")
    
    def _complete_task(self):
        """
        Update the self.completed attribute with current time
        """
        self.completed = self._get_time()
    
    def _cleanup_due_format(self):
        """
        Converts due date to a datetime object for sorting
        
        Additionally, cleans date string to a consistent format for clean printing (adds zeros)
        
        For example, converts
        9/3/2023 to 09/03/2023
        """
        # error check input
        date_components = self.due.split('/')
        if len(date_components) != 3:
            raise ValueError("Invalid date format")
        
        # add zeros on single digit days and months
        month, day, year = date_components
        formatted_month = month.zfill(2)
        formatted_day = day.zfill(2)
        datestring = f'{formatted_month}/{formatted_day}/{year}'
        
        # convert to a datetime object and output in desired format, MM/DD/YYY
        datetime_object = datetime.datetime.strptime(datestring, '%m/%d/%Y')
        self.due = datetime_object.strftime('%m/%d/%Y')


class Tasks:
    """A list of `Task` objects."""
    def __init__(self):
        self.tasks = []
        self.current_time = datetime.datetime.now()
        # read pickled Tasks object list into a list 
        try:
            with open('.todo.pickle', 'rb') as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            # pickling of newly created objects list is done just before exiting the program
            pass
        self._compute_task_ages()
        
    def _compute_task_ages(self):
        """Populate task ages. Called at instantiation of tasklist"""
        for task in self.tasks:
            time_delta = self.current_time - task.created_time_obj
            # Get the delta in days
            delta_days = time_delta.days
            # Format the delta in days as a string
            task.age = f"{delta_days}d"
        
    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open('.todo.pickle', 'wb') as file:
            pickle.dump(self.tasks, file)

    def list(self):
        """
        Console print a sorted list of outstanding tasks.
        
        SORT PRIORITY:
        -due dated tasks: by earliest date due
        -nondated tasks: by priority number
        """
        
        # make sublists
        uncompleted_tasks = list(filter(lambda task: task.completed == None, self.tasks))
        uncompleted_with_due_date = list(filter(lambda task: task.due != None, uncompleted_tasks))
        uncompleted_no_due_date = list(filter(lambda task: task.due == None, uncompleted_tasks))
        
        # sort sublists and then join them
        dated_sorted = sorted(uncompleted_with_due_date, key=lambda task: task.due)
        no_due_date_sorted = sorted(uncompleted_no_due_date, key=lambda task: task.priority)
        sorted_task_list = dated_sorted + no_due_date_sorted
        
        # specify task object attributes to print
        table = [[task.id, task.age, task.due, task.priority, task.name] for task in sorted_task_list]
        print('\n')
        print(tabulate(table, headers=['ID', 'Age', 'Due Date', 'Priority', 'Task'], numalign="left", tablefmt="simple_outline"))
        print('\n')
        
    def report(self):
        """
        Console print a sorted report of ALL tasks.
        
        SORT PRIORITY:
        -due dated tasks: by earliest date due
        -nondated tasks: by priority number
        """
        # separate list by <has due date>
        tasks_with_due_date = list(filter(lambda task: task.due != None, self.tasks))
        tasks_missing_due_date = list(filter(lambda task: task.due == None, self.tasks))
        
        # sort sublists and then join them
        dated_sorted = sorted(tasks_with_due_date, key=lambda task: task.due)
        no_due_date_sorted = sorted(tasks_missing_due_date, key=lambda task: task.priority)
        sorted_task_list = dated_sorted + no_due_date_sorted
        
        # specify task object attributes to print
        table = [[task.id, task.age, task.due, task.priority, task.name, task.created, task.completed] for task in sorted_task_list]
        print('\n')
        print(tabulate(table, headers=['ID', 'Age', 'Due Date', 'Priority', 'Task', 'Created', 'Completed'], numalign="left", tablefmt="simple_outline"))
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
        
    def delete(self, task_id):
        """
        Removes a task object from the tasklist.
        Error checking to ensure that the ID# specified by user exists in the takslist 
        """
        # Error check ID#
        if task_id not in [task.id for task in self.tasks]:
            print("That is not one of the ID's in the tasklist. Use --report to see a list of valid task ID's\n")
        else:
            [self.tasks.remove(task) for task in self.tasks if task.id == task_id]
            print(f'Deleted task {task_id}\n')
        
    def query(self, search_terms):
        """
        Return non-completed tasks that contain query terms
        """
        # remove capitalization for string compare
        search_terms = [term.lower() for term in search_terms]
        uncompleted_tasks = list(filter(lambda task: task.completed == None, self.tasks))    
        qeuried_tasks = []
        for term in search_terms:
            term_matches = list(filter(lambda task: term in task.name, uncompleted_tasks))
            qeuried_tasks = qeuried_tasks + term_matches
        
        # split list on <contains due date>   
        with_due_date = list(filter(lambda task: task.due != None, qeuried_tasks))
        no_due_date = list(filter(lambda task: task.due == None, qeuried_tasks))
        
        # sort sublists, then join them
        dated_sorted = sorted(with_due_date, key=lambda task: task.due)
        no_due_date_sorted = sorted(no_due_date, key=lambda task: task.priority)
        sorted_query_tasks = dated_sorted + no_due_date_sorted

        # specify task object attributes to print
        table = [[task.id, task.age, task.due, task.priority, task.name] for task in sorted_query_tasks]
        print('\n')
        print(tabulate(table, headers=['ID', 'Age', 'Due Date', 'Priority', 'Task'], numalign="left", tablefmt="simple_outline"))
        print('\n')
        
    def add(self, new_task):
        """Add a task to the tasklist and console print the ID#"""
        self.tasks.append(new_task)
        print(f'Created task {new_task.id}\n')
    
    def _get_new_task_id(self):
        """
        Generate a new unique ID#. Returns 1 if the list has not been created yet
        """
        # 0 if no tasks have been created, otherwise retrieve the MAX(task.id)
        highest_task_id = 0 if not self.tasks else max(self.tasks, key=lambda task: getattr(task, 'id')).id
        return highest_task_id + 1

def main():
    """
    Main loop for TODO list software.
    """
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
    
    # unpickle tasklist
    tasklist = Tasks()
    
    # User verb options:
    if args.add:
        # Instantiate a new task object
        new_task = Task(name=args.add,
                        priority=args.priority,
                        due=args.due,
                        unique_id=tasklist._get_new_task_id())
        # add new task to the existing tasklist
        tasklist.add(new_task)
    elif args.query:
        tasklist.query(args.query)
    elif args.list:
        tasklist.list()
    elif args.done:
        tasklist.done(args.done)
    elif args.delete:
        tasklist.delete(args.delete)
    elif args.report:
        tasklist.report()
    
    # pickle modified tasklist and exit
    tasklist.pickle_tasks()
    exit()

if __name__ == "__main__":
    main()
    
