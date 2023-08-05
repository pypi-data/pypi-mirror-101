from pathlib import Path

import click
from click_shell import shell

from ucentral import __version__
from ucentral.ucentral import Ucentral

uc = Ucentral()


@shell(prompt=">> ")
def cli():
    print(f"ucentral cli v{__version__}")
    schema_path = Path.cwd() / "ucentral.schema.json"
    if schema_path.is_file():
        uc.schema_load(schema_path)
        print("Loaded schema `ucentral.schema.json`")
    else:
        print("No schema loaded, please run `schema-load <filename>`")


@cli.command()
def show():
    """Show current configuration"""
    print(uc.show())


@cli.command()
@click.argument("path")
@click.argument("value")
def set(path, value):
    """Set <path> to <value>"""
    print(uc.set(path, value))


@cli.command()
@click.argument("path")
@click.argument("filename", type=click.Path(exists=True))
def file(path, filename):
    """Set <path> to content of <filename>"""
    print(uc.file(path, filename))


@cli.command()
@click.argument("path")
@click.argument("filename", type=click.Path(exists=True))
def base64(path, filename):
    """Set <path> to base64 encoded content <filename>"""
    print(uc.base64(path, filename))


@cli.command()
@click.argument("path")
def add(path):
    """ Add an anonymous obejct to the given configuration."""
    print(uc.add(path))


@cli.command()
@click.argument("path")
def get(path):
    """Return value from <path>"""
    print(uc.get(path))


@cli.command()
@click.argument("path")
@click.argument("value")
def add_list(path, value):
    """Add the given value to an existing list option."""
    print(uc.add_list(path, value))


@cli.command()
@click.argument("path")
@click.argument("value")
def del_list(path, value):
    """Delete element <value> from list at <path>"""
    print(uc.del_list(path, value))


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def load(filename):
    """Load configuration from JSON at <filename>"""
    print(uc.load(filename))


@cli.command()
@click.argument("filename", type=click.Path(writable=True))
def write(filename):
    """Store configuration as JSON at <filename>"""
    print(uc.write(filename))


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def schema_load(filename):
    """Load JSON schema from <filename>"""
    print(uc.schema_load(filename))
