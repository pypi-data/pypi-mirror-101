#!/usr/bin/env python

import click
import os
import driver
import projects
import utils
from DriverArgument import DriverArgument

# OPEN PROJECT DATA FILE

def get_project_titles(ctx, args, incomplete):
    """CLI autocomplete callback for project titles"""
    return [("""'{}'""".format("title")) for k in projects.open_projects() if incomplete in k["title"]]


@click.group()
def lmp():
    """A CLI wrapper for LaunchMyProject"""
    pass

@lmp.command()
def li():
    """List all projects."""

    curr_projects = projects.open_projects()

    if(len(curr_projects) == 0):
        click.echo("There are no created projects. Created projects are listed here.")

    for x,y,z in zip(curr_projects[::3], curr_projects[1::3], curr_projects[2::3]):
        click.echo("{:<30}{:<30}{:<}".format(x["title"],y["title"],z["title"]))


@ click.argument('project_title', type=click.STRING, autocompletion=get_project_titles)
@lmp.command()
def info(project_title: str):
    """Display details about a project"""
    project = projects.find_project(project_title)
    if  project != None:
        projects.print_details(project)
    else:
        click.echo("Unable to find a project of the name '{}'.".format(project_title))


@click.option('-Q', '--quit_console', is_flag=True, default=False, help='Process terminates shell after execution.')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Provide more verbose detail about started project.')
@click.option('-l', '--limited', is_flag=True, default=False, help='Launch only code editor.')
@click.argument('project_title', type=click.STRING, autocompletion=get_project_titles)
@lmp.command()
def start(project_title: str, quit_console: bool, verbose: bool, limited: bool):
    """Start project <PROJECT_TITLE>"""
    print("STARTING")
    project = projects.find_project(project_title)
    if project == None:
        click.echo(message='"{}" is not a known project. Try "lmp li" to see a list of prrojects'.format(project_title))
        return
    click.echo("Starting {}".format(project["title"]))

    if(verbose):
        click.echo(project["summary"])
# vimplug
    arg = DriverArgument()
    arg.make_start(project=project,limited=limited,quit=quit_console)

    driver.parse(arg)


@ lmp.group()
def config():
    """ A Wrapper for adding, removing, and configuring projects """
    pass


@ config.command()
def add():
    """ Goes through the process of adding a project to the project list """
    click.echo("Creating a new project.")

    # Create new project
    title: str = input("Project title? ")

    # Check if project already exists
    if projects.find_project(title) != None:
        overwrite: bool = utils.truthy_question("A project named '{}' already exists. Would you like to replace it?".format(title))
        if(not overwrite):
            click.echo("Project creation terminated by user.")
            return
        rmArg = DriverArgument()

        project_rm = projects.find_project(title)

        rmArg.make_rm(project=project_rm, projects=projects.open_projects())
        driver.parse(rmArg)
      

    summary = click.prompt(text="Project summary? ")
    os = driver.get_plat()
    path = click.prompt(text="Absolute path to project: ")

    if(not driver.is_pathname_valid(path)):
        if(not utils.truthy_question("Provided path is invalid, continue anyway? (y/n)")):
            driver.__exit("Process terminated.")

    editor_cmd: str = click.prompt(
        text='Command to open editor (use "code" to open vscode): ')

    CMDS: bool = click.confirm(
        "Would you like to add any run time commands?")
    
    cmds: list = []
    if(CMDS):
        while True:
            cmd = input('Enter command. (Enter "end" to end)')
            if(cmd.lower() == "end"):
                break
            cmds.append(cmd)

    project_to_add = {
        "title": title,
        "summary": summary,
        "os": {
            "{}".format(os): {
                "path": path,
                "editor-cmd": editor_cmd,
                "scripts": {
                    "cmds": cmds,
                    "bash-scripts": []
                }
            }

        }
    }

    arg = DriverArgument()
    arg.make_add(project=project_to_add, projects=projects.open_projects())
    
    success: bool = driver.parse(arg)
    if success:
        click.echo("'{}' created successfully".format(title))


@ click.argument('project_title')
@ config.command()
def rm(project_title: str):
    """ Goes through the process of removing a project from the project list """

    project_to_remove = projects.find_project(project_title)

    arg = DriverArgument()
    arg.make_rm(project=project_to_remove,projects=projects.open_projects())
    
    driver.parse(arg)

   
@ click.argument('project_title')
@ config.command()
def edit(project_title: str):
    """ Goes through the process of editing a project in the project list """
    project_to_edit = projects.find_project(project_title)
    projects.print_details(project_to_edit)
    FIELDS = ["title", "summary", "path", "editor-cmd", "cmds"]
    field = input("Choose field to edit: ").lower()

    while (not (field in set(FIELDS))):
        field = input('Invalid field "{}": '.format(field)).lower()

    arg = DriverArgument()
    arg.make_edit(project=project_to_edit, projects=projects.open_projects(),field=field)
    driver.parse(arg)


if __name__ == '__main__':
    lmp(prog_name="lmp")
