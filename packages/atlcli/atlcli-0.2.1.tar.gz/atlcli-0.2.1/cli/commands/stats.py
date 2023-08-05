import os, sys
import click
import json
from services import ConfluenceService

verifyssl = False

@click.group()
@click.pass_context
def stats(ctx):
    context_parent = click.get_current_context(silent=True)
    ctx.ensure_object(dict)
    ctx.obj['bitbucket_url'] = context_parent.obj["bitbucket_url"]
    ctx.obj['jira_url'] = context_parent.obj["jira_url"]
    ctx.obj['confluence_url'] = context_parent.obj["confluence_url"]
    ctx.obj['username'] = context_parent.obj["username"]
    ctx.obj['password'] = context_parent.obj["password"]
    verifyssl = context_parent.obj["verifyssl"]
    pass


@stats.command()
@click.pass_context
@click.option('-j', '--project-key', required=True, default="", help="Project key used in your Jira project.")
@click.option('--format', required=False, default="", help="Specify in with file format you want the data")
@click.option('--average/--no-average', required=False, default="", help="Get average result in the console.")
def releases(ctx, project_key, format, average):
    pass


@stats.command()
@click.pass_context
@click.option('-v', '--version', required=False, default="", help="Specify version if you want statistics about a version.")
@click.option('-j', '--project-key', required=True, default="", help="Project key used in your Jira project.")
@click.option('--json/--no-json', required=False, default=False, help="Provides stats in json format.")
def tickets(ctx, version, project_key, json):
    pass

@stats.command()
@click.option('-j', '--project-key', required=True, default="", help="Project key used in your Jira project.")
@click.pass_context
def products(ctx, project_key):
    pass
