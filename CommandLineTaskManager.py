#!/usr/bin/env python3
"""Command Line Task Manager"""
# an object oriented task manager application that 
# user can enter tasks, save them to a file, and retrieve


# Task Class -- A Single Task
# Requirements: 
    # 1. Each task can be uniquely identified by a numeric identifier. -- UUID
    # 2. Tasks have diff. priority levels 123 (3 is the highest priority).
    # 3. A Task object should store the date they were created and completed
    # 4. allows for different types of tasks: a task with no due date and a task with a due date.

import argparse
import pickle
import datetime #Module7 Problem4

class Task:
  """Representation of a task
  
  Attributes:
              - created - date
              - completed - date
              - name - string
              - unique id - number
              - priority - int value of 1, 2, or 3; 1 is default
              - due date - date, this is optional
  """
  def __init__(self, name, priority=1, due_date=None):
        self.unique_id = None 
        self.created = datetime.datetime.today()  # help(datetime), https://docs.python.org/3.9/library/datetime.html
        
        # fix due_date errors:
        # AttributeError: 'str' object has no attribute 'strptime'
        # TypeError: '<' not supported between instances of 'str' and 'datetime.datetime'
        if isinstance(due_date, str):  # not None
            try:
                #  parse the due_date string to a datetime object, otherwise Error!!!
                self.due_date = datetime.datetime.strptime(due_date, '%m/%d/%Y')
            except AttributeError or ValueError: 
                print(f"Error when parsing due date: {due_date}")
                self.due_date = None  # Set due_date to None if there's a Error
        elif isinstance(due_date, datetime.datetime):
            self.due_date = due_date
        else:
            self.due_date = None

        self.completed = None
        self.name = name
        self.priority = priority
        
  def mark_completed(self): # mark completed date 
        self.completed = datetime.datetime.today()

  def TaskRepresentation(self): # ***
        return f"Task({self.name}, priority={self.priority}, due_date={self.due_date}, completed={self.completed}"
        

# Tasks Class
    # Implement a Tasks objects that have all the Task objects. 
    # Tasks should be implemented as a list of Task objects. - use list() to hold Task objects. 
    # The list should be ordered by the creation date. While running, the program should only have a single instance of Tasks.
    # implement all the methods that support the add, delete, list, report, query and done commands described below

class Tasks:
    """A list of `Task` objects."""
    
    def __init__(self):
        """Read pickled tasks file into a list"""
        # List of Task objects
        #Unpickle the file, if it exists
        try:
            with open('.todo.pickle','rb') as f:
                self.tasks = pickle.load(f) #load the data in to be used in our application
        except (EOFError, FileNotFoundError):
            self.tasks = [] 
            

    def pickle_tasks(self):
        """Picle your task list to a file"""
        with open('.todo.pickle','wb') as f:
            pickle.dump(self.tasks, f)
            
  # Complete the rest of the methods, change the method definitions as needed        

    def add(self, name, priority=1, due_date=None):
        """ Add new task""" 
        task_unique_id = len(self.tasks)+1 # assign unique id to each task. the next generated ID is current tasks' length +1
        add_task = Task(name, priority, due_date)
        add_task.unique_id = task_unique_id # set the unique_id i
        self.tasks.append(add_task)
        self.pickle_tasks()  # update pickle; calling the function
        print(f"Successfully added task:\n Unique ID: {task_unique_id}\n Name: {name}\n Priority: {priority}\n Due: {due_date}")

     
    def list(self):
        """ Display a list of the not completed tasks sorted by the due date"""
            # if same due date, sort by decreasing priority (1 is the highest priority)
            # if no due date, then sort by decreasing priority. 123 
        
        #filter those incomplted tasks
        incomplete_tasks = [task for task in self.tasks if not task.completed]

        # Sort based on due date & priority(high to low = 1-2-3)
            # 1- assign a max date to those w/o due date, making them rank in the end
        for task in incomplete_tasks:
            # Debug due_date TypeError:
            # print(f"Debug: Task ID {task.unique_id}, due_date type: {type(task.due_date)}, due_date value: {task.due_date}")
            
            if task.due_date is None:
                task.due_date = datetime.datetime.max 
                
            # 2- if same due date, sort by decreasing priority: 123(small number first)
        incomplete_tasks.sort(key=lambda x: (x.due_date, -x.priority)) 
  
        # Go thro the incompleted tasks list, & Print the chart.
        print("ID Age  Due Date Priority  Task")
        print("-- ---  -------- --------  -----")
        for task in incomplete_tasks:
            # The Age in the table is the number of days since the task was created.
            age = (datetime.datetime.today() - task.created).days 
            
            if task.due_date == datetime.datetime.max: # if due date is assigned a max value, convert it back to '-'
                due_date = '-'
            else:
                due_date = task.due_date.strftime('%m/%d/%Y')

            print(f"{task.unique_id:<3}  {age:<3}  {due_date:<11}  {task.priority:<5} {task.name})")
            # {:<5}to reserve enough string space

    
    def query(self, terms):
        """Search for tasks that match a search term"""
        # Only return tasks are not completed. Muliple terms should be able to be searched.
        # Multiple values for a single argument: using argparse package, nargs ='+'
        # ensure upper or lowercase search are ok

        # find those incompelted tasks, that match the serch term:
        match_tasks = [] 
        match_task_ids = set() # in case same task name
        for term in terms:
            for task in self.tasks:
                if not task.completed and term.lower() in task.name.lower():
                    if task.unique_id not in match_tasks:
                        match_tasks.append(task)
                        match_task_ids.add(task.unique_id) # carry along w/ unique id       

        # Go thro the matched tasks list, & Print the chart.
        if match_tasks:
            print("ID Age  Due Date       Priority  Task")
            print("-- ---  ------------   --------  ----")
            for task in match_tasks:  
                age = (datetime.datetime.today() - task.created).days 
            
                if task.due_date: # if due date exists (True)
                    due_date = task.due_date.strftime('%m/%d/%Y')
                else:
                    due_date = '-'         
                print(f"{task.unique_id:<3} {age:<5} {due_date:<10} {task.priority:<3} {task.name}")
        else:
            print("No matched tasks found.")

    
    def done(self, task_id): # set the variable task_id
        """Mark a task as Complete: by passing the done argument and the unique identifier. """
        # not deleting a task, just marking as complete.  
        #Your --list methods should ensure that it not longer is printed to the terminal.

        # iterate the tasks to check if inputed task_id can match unique_id: E.g --done 1  >>>> Completed task 1
        task = None
        for t in self.tasks:
            if t.unique_id == task_id: 
                task = t  
                break

        # change a single task's status to complete by giving it a complted date 
        if task and not task.completed: # ensure task is not None, and some tasks incompleted
            task.mark_completed() # call the function, giving it a complted date 
            self.pickle_tasks()
            print(f"Completed task {task.unique_id}")
        else:
            print(f"Task {task_id} not found in the tasks list.")

    
    def delete(self, task_id): # set the variable task_id
        """Delete a task by passing the --delete command and the unique identifier. """
        # iterate the tasks to check if inputed task_id can match unique_id: E.g --done 1  >>>> Completed task 1
        task = None
        for t in self.tasks:
            if task.unique_id == task_id: 
                task = t   
                break

        try:
            self.tasks.remove(task)
            self.pickle_tasks()
            print(f"Deleted task {task.unique_id}")
        except ValueError:
            print(f"Task with ID {task.unique_id} not found in the task list.")     
            

    def report(self):
        """List all tasks, both completed and incomplete tasks. """
        # Follow the required formatting for the the output. Follow the same reporting order as the --list command.

        # Sort based on due date & priority(high to low = 1-2-3). Sorted() -- create new list, leaving the org. list unchanged
        for task in self.tasks:
            if task.due_date is None:
                task.due_date = datetime.datetime.max

        sorted_tasks = sorted(self.tasks, key=lambda x: (x.due_date, -x.priority))

        print("ID Age  Due Date   Priority     Task                       Created                         Completed   ")
        print("-- ---  --------   --------     ----                 -------------------------            ------------")

        for task in sorted_tasks:
            age = (datetime.datetime.today() - task.created).days 

            # due date covert from max to '-'
            if task.due_date == datetime.datetime.max:
                due_date = '-'
            else:
                due_date = task.due_date.strftime('%m/%d/%Y')

            # Created time
            Created = task.created.strftime('%a %b %d  %H:%M:%S %Z %Y')  
            # Mon Mar  5 12:10:08 CST 2018 
            # source: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            
            # Completed time
            Completed = task.completed.strftime('%a %b %d  %H:%M:%S %Z %Y') if task.completed else '-'
            print(f"{task.unique_id:<3} {age:<3} {due_date:<10} {task.priority:<10} {task.name:<22} {Created:<35} {Completed}")

                    
            # 1- assign a max date to those w/o due date, making them rank in the end



def parse_date(date_inputed):
    """Consistent users' date format"""
    date_formats = ['%d/%m/%Y', '%m/%d/%Y', '%d%m%Y', '%m%d%Y','%Y-%m-%d'] # if user input diff. format， e.g 22012024
    for date_format in date_formats:
        try:
            parsed_date = datetime.datetime.strptime(date_inputed, date_format) #2 parameters in strptime: (the string to be converted, the converted format)
            return parsed_date.strftime('%m/%d/%Y')
        except ValueError:
            continue
    raise ValueError(f"Unable to parse this date format. Please input in format MM/DD/YYYY.")
         

def main():
    """all the real work"""
    parser = argparse.ArgumentParser(description="Update your to do list.")
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list') #required = False is not necessary, user can optionally provide
    parser.add_argument('--due', type=str, required=False, help='set the due date MM/DD/YY for your task')
    parser.add_argument('--priority', type=int, required=False, help='priorize your task 1/2/3; default value is 1 - the highest')
    parser.add_argument('--list', action='store_true', required=False, help='List all incompleted tasks')
    parser.add_argument('--query', type=str, required=False, nargs="+", help='input your search terms to find related tasks')# unlimited terms w/ nargs="+"
    parser.add_argument('--done', type=int, required=False, help='mark a task as completed')
    parser.add_argument('--delete', type=int, required=False, help='delete a task')
    parser.add_argument('--report', action='store_true', required=False, help='report all tasks including both completed and incompleted')

    # parse the argument
    args = parser.parse_args()
    
    # read out arguments(note the types)
    tasks = Tasks()
    if args.add:
        due_date = None
        priority = args.priority if args.priority else 1
        if args.due: # if due not None, convert the date format
            due_date = parse_date(args.due)
        tasks.add(args.add, priority, due_date) 
            # calling add function in class Tasks, get the user's priority & due date 
    
    if args.list:  # CANNOT use elif, coz if Add is execute, other cannot be execute
        tasks.list() 

    if args.query:
        tasks.query(args.query) # need user to input paramenter 

    if args.done:
        tasks.done(args.done)

    if args.delete:
        tasks.delete(args.delete)

    if args.report:
        tasks.report()

if __name__ == "__main__":   
    main()
      

#example testing:
# python CommandLineTaskManager.py —- 
# add tasks:
#1 python CommandLineTaskManager.py --add "walk dog" --priority 3 --due 9/10/2024
#2 python CommandLineTaskManager.py --add "walk dog" --priority 3 --due 22102024
#3 python CommandLineTaskManager.py --add 'do homework' --priority 1 --due 22/06/2023
#4 python CommandLineTaskManager.py --add 'clean the room' --priority 2
#5 python CommandLineTaskManager.py --add 'wash dish' --priority 1 --due 22/06/2024

# complete:
# python CommandLineTaskManager.py --done 4      --ok >> Task 4 not found in the tasks list.

# incomplete:
# python CommandLineTaskManager.py --list        --- ok

# python CommandLineTaskManager.py --query dog dish  - ---ok
# python CommandLineTaskManager.py --report         --- ok