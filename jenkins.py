"""
Jenkins methods.

(c) 2018 Balloon Inc. VOF
Wouter Devriendt
"""
from pprint import pprint

import requests
import os


class Jenkins:
    def __init__(self, jenkins_url=None, username=None, auth_token=None):
        self.jenkins_url = jenkins_url
        self.username = username
        self.auth_token = auth_token

    def getAuth(self):
        return (self.username, self.auth_token)

    def startJob(self, job):
        url = self.jenkins_url+"/job/" + job + "/build"
        return requests.post(url, auth=self.getAuth())

    def abortJob(self, job):
        url = self.jenkins_url+"/job/" + job + "/lastBuild/stop"
        return requests.post(url, auth=self.getAuth())

    def getAllJobs(self):
        url = self.jenkins_url + "/api/json?tree=jobs[name]"
        return requests.get(url, auth=self.getAuth())

    def getJobStatus(self, job):
        url = self.jenkins_url + "/job/" + job + \
            "/lastBuild/api/json?tree=result,timestamp,estimatedDuration,number,building,duration"
        return requests.get(url, auth=self.getAuth())

    def readSettingsFromEnvironment(self):
        self.jenkins_url = os.environ["jenkins_url"]
        self.username = os.environ["jenkins_username"]
        self.auth_token = os.environ["jenkins_auth_token"]

    def readSettingsFromFile(self):
        import yaml
        with open("settings.yaml", 'r') as stream:
            try:
                settings = yaml.load(stream)
                self.jenkins_url = settings["jenkins_url"]
                self.username = settings["jenkins_username"]
                self.auth_token = settings["jenkins_auth_token"]
            except yaml.YAMLError as exc:
                print("Could not read settings.yaml")
                print(
                    "Verify if the file exists and has a correct syntax and has all necessary values filled in.")
                print("See settings.yaml.sample for what is needed.")
                print(exc)
                exit()


if __name__ == "__main__":
    import time
    jenkins = Jenkins()
    jenkins.readSettingsFromFile()

    r = jenkins.getAllJobs()
    # pprint(vars(r))

    r = jenkins.getJobStatus("sleep-test")
    # print(r.json())

    # Start the job
    r = jenkins.startJob("sleep-test")
    print(r.text)
    # time.sleep(5)

    # Get the job status every second
    for _ in range(6):
        r = jenkins.getJobStatus("sleep-test")
        print(r.json()["building"])
        time.sleep(2)
    exit()
    # Abort the job
    r = jenkins.abortJob("sleep-test")
    print(r.text)
