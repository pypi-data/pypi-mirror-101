from os.path import expanduser
import yaml
import base64

class ConfigurationManager:
    DEFAULT_CONFIG_FILE_PATH = expanduser("~")+"/.gdlf_config.yml"

    def __init__(self):
        pass

    def load_config(self):
        try:
            with open(self.DEFAULT_CONFIG_FILE_PATH) as file:
                data = yaml.safe_load(file, Loader=yaml.FullLoader)
            return data
        except IOError:            
            return None        
        

    def create_config(self, data):        
        with open(self.DEFAULT_CONFIG_FILE_PATH, 'w') as file:
            yaml.dump(data, file)

    def is_config_valid(self):
        try:
            with open(self.DEFAULT_CONFIG_FILE_PATH) as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                
                bitbucket_url_valid = "bitbucket-url" in data and data["bitbucket-url"]
                jira_url_valid = "jira-url" in data and data["jira-url"]
                confluence_url_valid = "confluence-url" in data and data["confluence-url"]
                credentials_valid = "credentials" in data and "username" in data["credentials"] and "password" in data["credentials"] and data["credentials"] and data["credentials"]

                is_valid = bitbucket_url_valid and jira_url_valid and confluence_url_valid and credentials_valid
                return is_valid
        except IOError:            
            return False        