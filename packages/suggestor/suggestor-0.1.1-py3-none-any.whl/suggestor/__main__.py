"""
"""

import click
import icecream


@click.command()
def main():
    """"""
    with open("banner.txt") as f:
        click.echo(f.read())
