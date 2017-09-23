# -*- condig: utf-8 -*-

import click

from sitic.config import config as conf
from sitic.utils import constants
from sitic.generator import Generator
from sitic.commands.watcher import Watcher
from sitic.commands.server import Server
from sitic.commands.makemessages import MakeMessages
from sitic.commands.compilemessages import CompileMessages
from sitic.commands.new_command import NewCommand
from sitic.commands.publish_command import PublishCommand
from sitic.commands.new_site_command import NewSiteCommand


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--config', default='sitic.yml', type=click.Path())
@click.option('--build_draft', is_flag=True, default=False, type=bool)
@click.option('--build_future', is_flag=True, default=False, type=bool)
@click.option('--build_expired', is_flag=True, default=False, type=bool)
def cli(ctx, config, build_draft, build_future, build_expired):
    """
    Sitic is a Static Site Generator built in Python.

    If no command is specified, the «generate» command will be executed
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(generate)


@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--build_draft', is_flag=True, default=False, type=bool)
@click.option('--build_future', is_flag=True, default=False, type=bool)
@click.option('--build_expired', is_flag=True, default=False, type=bool)
def generate(config, build_draft, build_future, build_expired):
    conf.load_config(config)
    conf.build_draft = build_draft
    conf.build_future = build_future
    conf.build_expired = build_expired
    generator = Generator()
    generator.gen()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--build_draft', default=False, type=bool)
@click.option('--build_future', default=False, type=bool)
@click.option('--build_expired', default=False, type=bool)
@click.option('--port', default=constants.DEFAULT_PORT, type=int)
def server(config, build_draft, build_future, build_expired, port):
    """
    Sitic provides its own webserver which builds and serves the site.
    It is a webserver with limited options.
    It is not recommended to use it in production, instead use more featured
    servers as nginx or apache.

    By default Sitic will also watch your files for any changes you make and
    automatically rebuild the site.
    """
    conf.load_config(config)
    conf.build_draft = build_draft
    conf.build_future = build_future
    conf.build_expired = build_expired
    server = Server(port)
    server.start()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--build_draft', default=False, type=bool)
@click.option('--build_future', default=False, type=bool)
@click.option('--build_expired', default=False, type=bool)
def watch(config, build_draft, build_future, build_expired):
    conf.load_config(config)
    conf.build_draft = build_draft
    conf.build_future = build_future
    conf.build_expired = build_expired
    watcher = Watcher()
    watcher.start()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
def makemessages(config):
    conf.load_config(config)
    maker = MakeMessages()
    maker.run()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
def compilemessages(config):
    conf.load_config(config)
    compiler = CompileMessages()
    compiler.compile()

@cli.command()
@click.argument('filepath')
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--title', default=None, type=str)
@click.option('--frontmatter', default='toml', type=click.Choice(['toml', 'yaml']))
def new(filepath, config, title, frontmatter):
    conf.load_config(config)
    new_command = NewCommand(filepath, title, frontmatter)
    new_command.run()

@cli.command()
@click.argument('filepath')
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
def publish(filepath, config):
    conf.load_config(config)
    command = PublishCommand(filepath)
    command.run()

@cli.command()
@click.argument('path')
def new_site(path):
    new_site = NewSiteCommand(path)
    new_site.run()
