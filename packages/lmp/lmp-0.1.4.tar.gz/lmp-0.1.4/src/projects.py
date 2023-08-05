from json.decoder import JSONDecodeError
import json
import driver
import os
import click

absPath = os.path.dirname(os.path.abspath(__file__))


def open_projects() -> list:
  try:
    with open("{}/projects.json".format(absPath), "x") as f:
        json.dump([], f)
  except FileExistsError:
    with open("{}/projects.json".format(absPath), "r+") as f:
        try:
            projects = json.load(f)
        except JSONDecodeError:
            json.dump([], f)
            projects = []
            pass
        f.close()
    pass
    return projects

def select_project(title: str, project_list: list) -> dict:
    for project in project_list:
        if project["title"].lower() == title.lower():
            return project
    return None


def find_project(project_title: str) -> dict or None:
    
    projects = open_projects()
    
    project = select_project(project_title, projects)
    if(project == None):
        return None
    return project

def create_project_struct(title: str, summary: str, os: str, path: str, editor_cmd: str, cmds: list):
    print("Creating Project")




def print_cmd_details(cmds: list):
    """Prints Commands """
    if(len(cmds) > 0):
        print("Runtime Commands:")
        for i in range(len(cmds)):
            print("{}. {}".format(i+1,cmds[i]))

def print_details(project: dict):
    """Prints details about a project"""
    click.echo("Title:\n\t{}".format(project["title"]))
    click.echo("Summary:\n\t{}".format(project["summary"]))

    plat = driver.get_plat()
    click.echo("Path:\n\t{}".format(project["os"][plat]["path"]))
    click.echo("IDE Keyword:\n\t{}".format(project["os"][plat]["editor-cmd"]))
    print_cmd_details(project["os"][plat]["scripts"]["cmds"])