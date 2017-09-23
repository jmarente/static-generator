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
@click.option('--config', default='sitic.yml', type=click.Path(), help="Filesystem path to config file")
@click.option('--build_draft', is_flag=True, default=False, type=bool, help="Include content marked as draft")
@click.option('--build_future', is_flag=True, default=False, type=bool, help="Include content with publication_date in the future")
@click.option('--build_expired', is_flag=True, default=False, type=bool, help="Include expired content")
@click.option('--disable_sitemap', is_flag=True, default=False, type=bool, help="Do not generate Sitemap")
@click.option('--disable_rss', is_flag=True, default=False, type=bool, help="Do not generate RSS")
@click.option('--disable_search', is_flag=True, default=False, type=bool, help="Do not generate search indexer")
@click.option('--remove_expired', is_flag=True, default=False, type=bool, help="Remove already published content in destination folder")
@click.option('--clean_destination', is_flag=True, default=False, type=bool, help="Completelty remove destination folder before generation")
def cli(ctx, config, build_draft, build_future, build_expired, disable_sitemap, disable_rss, disable_search, remove_expired, clean_destination):
    """
    Sitic is a Static Site Generator built in Python.

    If no command is specified, the «generate» command will be executed
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(generate)


@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True), help="Filesystem path to config file")
@click.option('--build_draft', is_flag=True, default=False, type=bool, help="Include content marked as draft")
@click.option('--build_future', is_flag=True, default=False, type=bool, help="Include content with publication_date in the future")
@click.option('--build_expired', is_flag=True, default=False, type=bool, help="Include expired content")
@click.option('--disable_sitemap', is_flag=True, default=False, type=bool, help="Do not generate Sitemap")
@click.option('--disable_rss', is_flag=True, default=False, type=bool, help="Do not generate RSS")
@click.option('--disable_search', is_flag=True, default=False, type=bool, help="Do not generate search indexer")
@click.option('--remove_expired', is_flag=True, default=False, type=bool, help="Remove already published content in destination folder")
@click.option('--clean_destination', is_flag=True, default=False, type=bool, help="Completelty remove destination folder before generation")
def generate(config, build_draft, build_future, build_expired, disable_sitemap, disable_rss, disable_search, remove_expired, clean_destination):
    """
    Generate your site from your contents
    """
    conf.load_config(config)
    conf.build_draft = build_draft
    conf.build_future = build_future
    conf.build_expired = build_expired
    conf.disable_search = disable_search
    conf.disable_sitemap = disable_sitemap
    conf.disable_rss = disable_rss
    conf.remove_expired = remove_expired
    conf.clean_destination = clean_destination
    generator = Generator()
    generator.gen()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True), help="Filesystem path to config file")
@click.option('--build_draft', is_flag=True, default=False, type=bool, help="Include content marked as draft")
@click.option('--build_future', is_flag=True, default=False, type=bool, help="Include content with publication_date in the future")
@click.option('--build_expired', is_flag=True, default=False, type=bool, help="Include expired content")
@click.option('--disable_sitemap', is_flag=True, default=False, type=bool, help="Do not generate Sitemap")
@click.option('--disable_rss', is_flag=True, default=False, type=bool, help="Do not generate RSS")
@click.option('--disable_search', is_flag=True, default=False, type=bool, help="Do not generate search indexer")
@click.option('--remove_expired', is_flag=True, default=False, type=bool, help="Remove already published content in destination folder")
@click.option('--clean_destination', is_flag=True, default=False, type=bool, help="Completelty remove destination folder before generation")
@click.option('--port', default=constants.DEFAULT_PORT, type=int)
def server(config, build_draft, build_future, build_expired, disable_sitemap, disable_rss, disable_search, remove_expired, clean_destination, port):
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
    conf.disable_search = disable_search
    conf.disable_sitemap = disable_sitemap
    conf.disable_rss = disable_rss
    conf.remove_expired = remove_expired
    conf.clean_destination = clean_destination
    server = Server(port)
    server.start()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True), help="Filesystem path to config file")
@click.option('--build_draft', is_flag=True, default=False, type=bool, help="Include content marked as draft")
@click.option('--build_future', is_flag=True, default=False, type=bool, help="Include content with publication_date in the future")
@click.option('--build_expired', is_flag=True, default=False, type=bool, help="Include expired content")
@click.option('--disable_sitemap', is_flag=True, default=False, type=bool, help="Do not generate Sitemap")
@click.option('--disable_rss', is_flag=True, default=False, type=bool, help="Do not generate RSS")
@click.option('--disable_search', is_flag=True, default=False, type=bool, help="Do not generate search indexer")
@click.option('--remove_expired', is_flag=True, default=False, type=bool, help="Remove already published content in destination folder")
@click.option('--clean_destination', is_flag=True, default=False, type=bool, help="Completelty remove destination folder before generation")
def watch(config, build_draft, build_future, build_expired, disable_sitemap, disable_rss, disable_search, remove_expired, clean_destination):
    """
    Watch filesystem for changes and recreate as needed
    """
    conf.load_config(config)
    conf.build_draft = build_draft
    conf.build_future = build_future
    conf.build_expired = build_expired
    conf.disable_search = disable_search
    conf.disable_sitemap = disable_sitemap
    conf.disable_rss = disable_rss
    conf.remove_expired = remove_expired
    conf.clean_destination = clean_destination
    watcher = Watcher()
    watcher.start()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
def makemessages(config):
    """
    Runs over the entire source tree of layouts directory and pulls out all strings marked for translation.
    It creates (or updates) a message file in the locales directory.
    After making changes to the messages files you need to compile them with compilemessages for use with the builtin gettext support.
    """
    conf.load_config(config)
    maker = MakeMessages()
    maker.run()

@cli.command()
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
def compilemessages(config):
    """
    Compiles .po files created by makemessages to .mo files for use with the built-in gettext support.
    """
    conf.load_config(config)
    compiler = CompileMessages()
    compiler.compile()

@cli.command()
@click.argument('filepath')
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
@click.option('--title', default=None, type=str)
@click.option('--frontmatter', default='toml', type=click.Choice(['toml', 'yaml']))
def new(filepath, config, title, frontmatter):
    """
    Create a new content in the specified path
    """
    conf.load_config(config)
    new_command = NewCommand(filepath, title, frontmatter)
    new_command.run()

@cli.command()
@click.argument('filepath')
@click.option('--config', default='sitic.yml', type=click.Path(exists=True))
def publish(filepath, config):
    """
    Mark specific content as published
    """
    conf.load_config(config)
    command = PublishCommand(filepath)
    command.run()

@cli.command()
@click.argument('path')
def new_site(path):
    """
    Create basic files structure for a sitic project
    """
    new_site = NewSiteCommand(path)
    new_site.run()
