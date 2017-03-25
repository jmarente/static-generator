# -*- condig: utf-8 -*-

import click

from sitic.config import config as conf
from sitic.generator import Generator
from sitic.watcher import Watcher
from sitic.server import Server
from sitic.utils import constants


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--verbose', default=False)
def cli(ctx, config, verbose):
    conf.load_config(config)
    conf.verbose = verbose
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
