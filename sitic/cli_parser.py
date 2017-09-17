# -*- condig: utf-8 -*-

import click

from sitic.config import config as conf
from sitic.utils import constants
from sitic.generator import Generator
from sitic.commands.watcher import Watcher
from sitic.commands.server import Server
from sitic.commands.makemessages import MakeMessages
from sitic.commands.compilemessages import CompileMessages


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--build_draft', default=False, type=bool)
@click.option('--build_future', default=False, type=bool)
@click.option('--build_expired', default=False, type=bool)
def cli(ctx, config, build_draft, build_future, build_expired):
    conf.load_config(config)
    conf.build_draft = build_draft
    conf.build_future = build_future
    conf.build_expired = build_expired
    if ctx.invoked_subcommand is None:
        generator = Generator()
        generator.gen()

@cli.command()
@click.option('--port', default=constants.DEFAULT_PORT, type=int)
def server(port):
    server = Server(port)
    server.start()

@cli.command()
def watch():
    watcher = Watcher()
    watcher.start()

@cli.command()
def makemessages():
    maker = MakeMessages()
    maker.run()

@cli.command()
def compilemessages():
    compiler = CompileMessages()
    compiler.compile()
