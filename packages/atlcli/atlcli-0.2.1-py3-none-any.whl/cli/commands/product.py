import os, sys
import click
import pprint36 as pprint
from services import JiraService, PowerBIService
from utils import CsvUtil

verifyssl = False

@click.group()
@click.pass_context
def product(ctx):    
    """Displays infos about a product"""
    context_parent = click.get_current_context(silent=True)
    ctx.ensure_object(dict)    
    ctx.obj['jira_url'] = context_parent.obj["jira_url"]    
    ctx.obj['username'] = context_parent.obj["username"]
    ctx.obj['password'] = context_parent.obj["password"]
    verifyssl = context_parent.obj["verifyssl"]
    pass

@product.command()
@click.pass_context
@click.option('-v', '--product-version', required=True, default=False)
@click.option('-j', '--project-key', required=True, default=False)
def info(ctx, product_version, project_key):
    """Provides info about a product release"""
    pass

@product.command()
@click.pass_context
def versions(ctx):
    """Lists all the deployed versions of a product"""
    print("lists product versions")
    # print(productName)
    context_parent = click.get_current_context()
    pass

@product.command()
@click.pass_context
@click.option('-v', '--product-version', required=True, default=False)
@click.option('-j', '--project-key', required=True, default=False)
@click.option('--changes/--no-changes', required=False, default=False)
@click.option('--confluence/--no-confluence', required=False, default=False)
def tickets(ctx, product_version, project_key, changes, confluence):
    """Lists all components of a product"""
    jira_service = JiraService(
        ctx.obj['jira_url'], ctx.obj['username'], ctx.obj['password'], ctx.obj['verifyssl'])

    product_version = product_version.strip()
    versionInfo = jira_service.get_project_version_infos(project_key,
                                                        product_version)

    if confluence:
        confMarkup = jira_service.get_issues_confluence_markup(project_key,
                                                              versionInfo["id"])
        print(confMarkup)
    else:
        output = "\nId: {0}\nName: {1}\nDescription: {2}\nReleased: {3}\nStart date: {4}\nRelease date: {5}\n"

        if versionInfo is not None:
            print("test")
            print(output.format(
                versionInfo["id"],
                versionInfo["name"],
                versionInfo["description"],
                versionInfo["released"],
                versionInfo["startDate"],
                versionInfo["releaseDate"]))

        if changes:
            output = jira_service.get_issues_printable(versionInfo["id"])
            print(output)


@product.command()
@click.pass_context
def info(ctx):
    """Displays info about a product"""

    print("product info here")

@product.command()
@click.pass_context
@click.option('-v', '--version', required=False, default="", help="Specify version if you want statistics about a version.")
@click.option('-j', '--project-key', required=True, default="", help="Project key used in your Jira project.")
@click.option('--json/--no-json', required=False, default=False, help="Provides stats in json format.")
@click.option('-p', '--powerbi-url', required=False, default="", help="Push data to a PowerBI Real Time Dataset if provided.")
@click.option('--all-releases/--no-all-releases', required=False, default=False, help="Produces stats for all the releases created in a product. (Run it only once)")
@click.option('--csv/--no-csv', required=False, default=False, help="Produces a csv file.")
@click.option('-s', '--since', required=False, default="", help="Specify start date for stats")
def stats(ctx, version, project_key, json, powerbi_url, all_releases, csv, since):
    """Displays statistics about a product"""
    powerbi_service = None
    powerbi_url = powerbi_url.strip()
    jira_service = JiraService(
    ctx.obj['jira_url'], ctx.obj['username'], ctx.obj['password'], ctx.obj['verifyssl'])
    result = jira_service.get_deploy_frequency(project_key, since)
    

    deploy_freq = result["deploy_freq"]
    deploy_freq_date = result["deploy_freq_date"]
    deploy_freq_per_release = result["deploy_freq_per_release"]

    print("Number of releases published: {0}\nDeployment frequency: {1} days".format(result["number_of_releases"],
                deploy_freq))
    
    if csv and all_releases:
        csv_util = CsvUtil()
        csv_util.create_product_stats_csv(deploy_freq_per_release.items())

    if len(powerbi_url) > 0 or all_releases is True:
        powerbi_service = PowerBIService(api_url=powerbi_url, verifyssl=ctx.obj['verifyssl'] )

    if version is not None and all_releases is False:
        leadtime = jira_service.get_leadtime_for_changes_per_version(project_key,version)
        s_lead_time = "Version: {0}\nLead time for changes: {1}".format(version, leadtime)
        print(s_lead_time)    

        if len(powerbi_url) > 0:
            release_info = jira_service.get_project_version_infos(project_key, version)

            powerbi_service.push_data(project_key, version, release_info["releaseDate"], leadtime, deploy_freq, deploy_freq_date)
            print("INFO: Data pushed to PowerBI")

    elif all_releases is True:
        commits_delta = jira_service.get_delta_first_and_last_commits_all(project_key)
        leadtimes_all = jira_service.get_leadtime_for_changes_for_all(project_key, since)
        storypoints_all = jira_service.get_total_story_points_all(project_key,since)
        
        powerbi_service.push_data_all(project_key, leadtimes_all, deploy_freq_per_release, storypoints_all,commits_delta)
    
