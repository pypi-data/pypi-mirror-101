#!/usr/bin/env python


import os

import json
import subprocess
import sys


from DriverArgument import DriverArgument
import utils

try:
    import applescript
except ImportError:
    """This exception is expected on non apple"""


def parse(arg: DriverArgument) -> bool:
    """Parses a DriverArgument object. Acts upon the DriverArgument action. 
    Returns True if successful, false otherwise"""

    action = arg.get_action()

    if(action == "ADD"):
        return add(new_project=arg.pl_project, projects=arg.pl_projects)
    if(action == "RM"):
        return rm(project=arg.pl_project, projects=arg.pl_projects)
    if(action == "EDIT"):
        return edit(project=arg.pl_project, projects=arg.pl_projects, field=arg.pl_field)
    if(action == "START"):
        return start(project=arg.pl_project, projects=arg.pl_projects, limited=arg.o_lim, quit=arg.o_quit)
    return False





def create_commands():
    """Create commands"""



def edit_project(project: dict, field: str):
    project_to_add = project
    os = utils.get_plat()
    
    if(project_to_add[field] != None):
        
        if(field == "title"):
            newVal = input("Enter new title. ")
            project_to_add['title'] = newVal
        elif(field == "summary"):
            newVal = input("Enter new summary. ")
            project_to_add['summary'] = newVal
        elif(project_to_add["os"][os][field] != None):
            project_to_add["os"][field] == os

            if(field == "path"):
                newVal = input("new path")
                project_to_add["os"][os]["path"] = newVal
            elif(field == "editor-cmd"):
                newVal = input("New editor cmd")
                project_to_add["os"][os]["editor-cmd"] = newVal

            elif(project_to_add["os"][os]["scripts"][field] != None):
                if(field == "cmds"):
                    newVal = input("Enter new cmd")
                    project_to_add["os"][os]["scripts"]["cmds"] = newVal
                elif(field == "cmds"):
                    newVal = input("Enter new cmd")
                    project_to_add["os"][os]["scripts"]["cmds"] = newVal
                else:
                    utils.__exit("Invalid field")

    return project_to_add

   


def write_to_projects(projects: list):
    absPath = os.path.dirname(os.path.abspath(__file__))
    with open("{}/projects.json".format(absPath), "w") as outfile:
        json.dump(projects, outfile)


def remove_project(projects: list, selected: dict):
    return [i for i in projects if not (i['title'] == selected['title'])]


def start(project: dict, projects, limited: bool, quit: bool):

    plat = utils.get_plat()
    path = project["os"][plat]["path"]

    if not utils.is_pathname_valid(path):
        utils.__exit("Invalid path provided")

    editor_cmd = project["os"][plat]["editor-cmd"]
    file_sys_cmd = project["os"][plat]["file-sys-cmd"]
    terminal_cmd = project["os"][plat]["terminal-cmd"]
    
    #fileSys = "explorer"
    #openTerminal = 'start cmd.exe /k "{} && cd {}"'.format(path[:2], path)

    if(limited):
        print("Launching in limited mode")
    print("From: $> {}".format(path))

    # Open Editor
    subprocess.Popen("{} {}".format(editor_cmd, path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if(limited):
        utils.__exit("Done in limited mode")

    # Open File System
    subprocess.Popen('{} {}'.format(file_sys_cmd, path), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Open cmd/terminal
    os.system(terminal_cmd)

    # Execute any scripts
    cmds = project["os"][plat]["scripts"]["cmds"]
    for cmd in cmds:
        if plat == "macOS":
            script = "cd {} && {}".format(path, cmd)
            applescript.tell.app('Terminal', 'do script "' + script + '"')
        elif plat == "windows": 
            os.system('start cmd.exe /k "{} && cd {} && {}"'.format(path[:2], path, cmd))
        elif plat == "Linux":
            print("Run commands on Linux not yet supported")
        else:
            utils.__exit("Unknown OS, please report. 0-1")

    if(quit):
        os.system(project["os"][plat]["terminal-exit-cmd"])



    print("Project opened")
    printArt("Happy Hacking")



def add(new_project: dict, projects: list) -> bool:
    """ Add a project to projects.json """
    projects.append(new_project)
    write_to_projects(projects)
    return True


def rm(project: dict, projects: list) -> bool:
    """ Removed a project from projects.json """

    new_list = remove_project(projects=projects, selected=project)
    write_to_projects(new_list)
    return True


def edit(project: dict, projects: list, field: str) -> bool:
    """ Edit a project in projects.json """
    newProject = edit_project(project=project, field=field)

    # Only remove after new details are recorded in case of user ending reconfig early.
    post_rm_list = remove_project(projects=projects, selected=project)

    post_rm_list.append(newProject)
    write_to_projects(post_rm_list)

    return True


def printArt(word: str):
    if(word == "Happy Hacking"):
        happyHacking = "\u001B[32m.  .             .  .      .         \n|__| _.._ ._   . |__| _. _.;_/*._  _ \n|  |(_][_)[_)\_| |  |(_](_.| \|[ )(_]\n       |  |  ._|                  ._|\n\u001B[0m"
        print(happyHacking)
    # print("Project {}, has started. Happy Hacking".format(title))
