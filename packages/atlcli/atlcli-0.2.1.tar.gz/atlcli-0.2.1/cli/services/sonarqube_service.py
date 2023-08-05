import urllib
import re
import sys,os
import ssl
import pprint36 as pprint
import base64
import requests
import json
from decimal import Decimal
from prettytable import PrettyTable

class SonarQubeService:
    
    def __init__(self, url, apikey, verify_ssl=True):
        self.api_url = "{0}/api".format(url)        
        self.api_url = self.api_url.replace("//api","/api")
        self.verify_ssl = verify_ssl        
        
        auth = "{0}:".format(apikey.strip())
        encodedBytes = base64.b64encode(auth.encode("utf-8"))
        self.api_auth = "Basic {0}".format(str(encodedBytes,"utf-8"))       
         

    def get_measures(self, project_key):        

        encoded_project_key = urllib.parse.quote(project_key)
        url = "{0}/measures/search".format(self.api_url)
        querystring = {
            "metricKeys":"coverage,reliability_rating,security_rating,sqale_rating,ncloc,files,uncovered_conditions,uncovered_lines,conditions_to_cover,lines_to_cover",
            "projectKeys":"{0}".format(project_key)
        }
        payload = ""
        headers = {
            'Content-Type': "application/json",
            'Authorization': self.api_auth
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        result = json.loads(response.text)

        parsed_measures = self.parse_measures(result["measures"])
        pass

    def parse_measures(self,measures):
        metrics = dict()

        coverage = next((x for x in measures if x["metric"] == "coverage"), None)["value"]
        metrics["coverage"] = dict()              
        metrics["coverage"]["color"] = self.get_coverage_color(coverage)
        metrics["coverage"]["value"] = coverage
        metrics["coverage"]["name"] = "Coverage"

        sqale = next((x for x in measures if x["metric"] == "sqale_rating"), None)["value"]
        metrics["sqale"] = dict()              
        metrics["sqale"]["color"] = self.get_number_color(sqale),
        metrics["sqale"]["value"] = self.get_number_letter(sqale),
        metrics["sqale"]["name"] = "Maintainability"
        

        reliability = next((x for x in measures if x["metric"] == "reliability_rating"), None)["value"]
        metrics["reliability"] = dict()
        metrics["reliability"]["color"] = self.get_number_color(reliability),
        metrics["reliability"]["value"] = self.get_number_letter(reliability),
        metrics["reliability"]["name"] = "Reliability"
        

        security =  next((x for x in measures if x["metric"] == "security_rating"), None)["value"]
        metrics["security"] = dict()
        
        metrics["security"]["color"] = self.get_number_color(security),
        metrics["security"]["value"] = self.get_number_letter(security),
        metrics["security"]["name"] = "Security"
        

        number_of_lines = next((x for x in measures if x["metric"] == "ncloc"), None)["value"]
        metrics["number-of-lines"] = dict()
        
        metrics["number-of-lines"]["color"] = "blue",
        metrics["number-of-lines"]["value"] = self.get_number_letter(number_of_lines),
        metrics["number-of-lines"]["name"] = "Number of lines"
        

        return metrics

    def get_coverage_color(self, coverage):
        coverage = Decimal(coverage)
        if coverage is None:
            return ""
        if coverage < 50: 
            return "red"
        if coverage < 60: 
            return "orange"
        if coverage < 70: 
            return "yellow"
        if coverage < 80: 
            return "olive"

        return "green"
            

    def get_number_color(self, number):
        if number is None:
            return ""

        if number == "1.0":
            return "green"

        if number == "2.0":
            return "olive"

        if number == "3.0":
            return "yellow"

        if number == "4.0":
            return "orange"

        if number == "5.0":
            return "red"

        return ""

    def get_number_letter(self, number):
        if number == "1.0": 
            return "A"

        if number == "2.0": 
            return "B"

        if number == "3.0": 
            return "C"

        if number == "4.0": 
            return "D"
            
        if number == "5.0": 
            return "E"
        
        return ""
