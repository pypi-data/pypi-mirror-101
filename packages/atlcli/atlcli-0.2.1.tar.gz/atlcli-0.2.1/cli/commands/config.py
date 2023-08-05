
import click
import os
from utils import ConfigurationManager

confManager = ConfigurationManager()


@click.command()
@click.option('--skipssl/--no-skipssl', prompt=True, required=True, default=False, help="Skips ssl validation in case you have certificates issues (not recommended)")
@click.option('--bitbucket-url', prompt=True, required=True, default="", help="Please enter the url for Bitbucket")
@click.option('--jira-url', prompt=True, required=True, default="", help=" Please enter the url for Jira")
@click.option('--confluence-url', prompt=True, required=True, default="", help="Please enter the url for Confluence")
@click.option('--username', prompt=True, required=True, default="", help="Username")
@click.option('--password', prompt=True, required=True, default="", hide_input=True, help="Password")
def config(skipssl, bitbucket_url, jira_url, confluence_url, username, password):
    """Configure Atlassian CLI for local use."""
    dict_file = dict()
    credentials = dict()
    confluence_config = dict()
    confluence_parentpages = dict()

    dict_file["bitbucket-url"] = bitbucket_url.strip()
    dict_file["jira-url"] = jira_url.strip()
    dict_file["confluence-url"] = confluence_url.strip()
    credentials["username"] = username.strip()
    credentials["password"] = password.strip()
    dict_file["credentials"] = credentials
    dict_file["verifyssl"] = skipssl

    confManager.create_config(dict_file)
    confManager.is_config_valid()

class HiddenPassword(object):
    def __init__(self, password):
        self.password = password
    def __str__(self):
        return '*' * len(self.password)