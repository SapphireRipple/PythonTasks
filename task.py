import json
import os
from datetime import datetime
# imported all modules

# sets file paths for tasks.json and log file for run
filePath = 'tasks.json'
home = os.environ.get("HOME")
logFileName = f"{home}/.local/practicalExerciseLogs/{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} Log.txt"

# if the task file path doesn't exist, create it
if not os.path.exists(filePath): 
    os.makedirs(filePath)

# open the tasks.json file and extract json data into taskData
with open('tasks.json', 'r') as taskFile:
    taskData = json.load(taskFile)

# make a list of task names sorted by their priority
newTaskListIndex = sorted(taskData, key=lambda x: taskData[x]['priority'])

# copy of the index list
taskListCopy = newTaskListIndex.copy()

# creates a dictionary of all tasks, sets value of all to "pending"
tasksDone = {}
def set_all_pending():
    for t in taskData:
        tasksDone[t] = 'pending'
set_all_pending()

# function that writes into the log file
def writeIntoFile(command):
    with open(logFileName, "a") as file:
        file.write(command)

# finishes task by making sure that the task has a command, writing into log and printing it, then setting as done
def finishTask(task):
    if taskData[task]['command'] != False:
        writeIntoFile(f"{taskData[task]['command']}\n")
        print(taskData[task]['id'], taskData[task]['command'], taskData[task]['dependencies'], taskData[task]['priority'])
        tasksDone[task] = 'done'
        taskListCopy.remove(task)
    else:
        print("There is no command for this task!")

# checks if the task has any dependencies, returns all if so
def has_dependency(task): 
    if taskData[task]['dependencies'] == []:
        return False
    else:
        return taskData[task]['dependencies']

# returns names of all dependencies of a task
def list_of_dependencies(task):
    dependencies_names = []
    for d in has_dependency(task):
        for t in taskData:
            try:
                if taskData[t]['id'] == d:
                    dependencies_names.append(t)
            except:
                print("There is no ID on the task!")
    return dependencies_names

# iterates until there are no more tasks
while not taskListCopy == []:
    for task in sorted(taskListCopy, key=lambda x: taskData[x]['priority']):
        # if there's no dependencies, just execute the task
        if not has_dependency(task):
            if not tasksDone[task] == 'done':
                finishTask(task)
                break
                
        # otherwise, find if it's dependencies have completed themselves
        else:
            dependency = False
            dependencies_names = []
            for depend in list_of_dependencies(task):
                if not tasksDone[depend] == 'done':
                        dependency = True
                        break
                if not dependency:
                    if not tasksDone[task] == 'done':
                        finishTask(task)
                        break
