from datetime import date
import csv

class CsvUtil:
    def __init__(self, path=None):
        if path is None:
            self.path = "./"
        else:
            self.path = path
    
    def create_product_stats_csv(self, stats_data):        
        header = ["Release","DeploymentFrequency","ReleaseDate"]
        file_suffix="_deploymentFrequencies"
        self.create_csv_file(stats_data, header, file_suffix )
     

    def create_csv_file(self, data, header, file_suffix=""):        
        today = date.today()
        s_date = today.strftime("%Y-%m-%d")
        file_path = "{0}/csv_{1}{2}.csv".format(self.path, s_date, file_suffix)

        with open(file_path, "w") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=",")
            filewriter.writerow(header)

            for key, sd in data:
                data_line = [key, sd["deploy_freq"], sd["releaseDate"]]
                filewriter.writerow(data_line)

       

# CSV generation
    # print("Release,Deployment-frequency,Date")

    # for key, f in deploy_freq_per_release.items():
    #     print("{0},{1},{2}".format(key,f["deploy_freq"],f["releaseDate"]))