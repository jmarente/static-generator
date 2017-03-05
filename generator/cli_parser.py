# -*- condig: utf-8 -*-
import click

from generator.config import config as conf
from generator.generator import Generator


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--config', default='config.yml', type=click.Path(exists=True))
@click.option('--verbose', default=False)
def cli(ctx, config, verbose):
    conf.load_config(config)
    conf.verbose = verbose
    if ctx.invoked_subcommand is None:
        click.echo('Call basic generator')
        generator = Generator()

@cli.command()
@click.option('--port', default=80, type=int)
def server(port):
    conf.port = port
    print("TODO server")

@cli.command()
def watch():
    print("TODO watch")
