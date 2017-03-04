# -*- condig: utf-8 -*-
import click

from generator.config import Config


@click.group(invoke_without_command=True)
@click.option('--config', default='config.yml', type=click.Path(exists=True))
def cli(config):
    Config.load_config(config)

@cli.command()
@click.option('--port', default=80, type=int)
def server(port):
    Config.set_port(port)
