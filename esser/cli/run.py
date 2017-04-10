import click
from esser.cli import BaseProject


@click.group()
def main():
    pass


@main.command()
@click.argument('project_dir')
def startproject(**kwargs):
    project = BaseProject(**kwargs)
    project.create()


if __name__ == '__main__':
    main()
