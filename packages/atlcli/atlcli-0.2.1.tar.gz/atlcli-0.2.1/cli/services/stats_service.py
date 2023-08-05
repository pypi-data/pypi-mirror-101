from dateutil import parser as date_parser
from datetime import datetime
import re
import math

class StatsService:
    
    def __init__(self):
        pass

    def calculate_deploy_frequency(self, releases):        
        number_of_diffs = 0
        sum_of_diffs = 0

        if len(releases) == 1:
            return 0

        for index, r in enumerate(releases):
            if index > 0:
                number_of_diffs += 1
                date1 = date_parser.parse(releases[index]["releaseDate"], fuzzy=True)
                date2 = date_parser.parse(releases[index-1]["releaseDate"], fuzzy=True)
                sum_of_diffs +=abs((date1 - date2).days)
            
        
        average = sum_of_diffs / number_of_diffs
        
        return average


    def calculate_deploy_frequency_per_release(self, releases):        
        deploy_freq_per_release = dict()
        
        releases = sorted(releases, key=lambda x: datetime.strptime(x["releaseDate"], '%Y-%m-%d'), reverse=False)

        for index, r in enumerate(releases):
            deploy_freq = self.calculate_deploy_frequency(releases[:(index+1)])
            deploy_freq_per_release[releases[index]["name"]] = dict()
            deploy_freq_per_release[releases[index]["name"]]["deploy_freq"] = deploy_freq
            deploy_freq_per_release[releases[index]["name"]]["releaseDate"] = r["releaseDate"]

        # for index, r in enumerate(releases):
              
        
        return deploy_freq_per_release

    def count_number_of_deploy_per_month(self, project_key, month=None):
        if(month is None):
            print("count number of deploys made in current month")
        else:
            print("count number of deploys made in specified month")
        pass

    def calculate_lead_time_for_changes(self, release, issues, latest_commits):        
        release_date = date_parser.parse(release["releaseDate"], fuzzy=True)
        issues_time_to_release = dict()
        s_date = ""
        lead_time_for_changes = 0
        sum_of_diffs = 0

        for key in latest_commits:            
            commit = latest_commits.get(key)
            m = re.search("^(\d{4}\-(0?[1-9]|1[012])\-\d{2})", commit["authorTimestamp"])

            if m:
                s_date = m.group(1)
                
            commit_date = date_parser.parse(s_date, fuzzy=True)
            sum_of_diffs+= abs((commit_date - release_date).days)            
        
        # TODO: replace date for when the ticket started to be in progress
        if len(latest_commits) != 0:
            lead_time_to_release = sum_of_diffs / len(latest_commits)
            return lead_time_to_release
        else:
            return -1
            
