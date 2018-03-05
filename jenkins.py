"""
Jenkins methods.

(c) 2018 Balloon Inc. VOF
Wouter Devriendt
"""
import requests
import os
from fuzzywuzzy import process

class Jenkins:
    def __init__(self, jenkins_url=None, username=None, auth_token=None, jobs=[]):
        self.jenkins_url = jenkins_url
        self.username = username
        self.auth_token = auth_token
        self.jobs = jobs

    def getAuth(self):
        return (self.username, self.auth_token)

    def startJob(self, jobname):
        url = self.jenkins_url+"/job/" + jobname + "/build"
        return requests.post(url, auth=self.getAuth())

    def abortJob(self, jobname):
        url = self.jenkins_url+"/job/" + jobname + "/lastBuild/stop"
        return requests.post(url, auth=self.getAuth())

    def getAllJobs(self):
        if not self.jobs:
            self.refetchAllJobs()
        return self.jobs

    def refetchAllJobs(self):
        url = self.jenkins_url + "/api/json?tree=jobs[name]"
        r = requests.get(url, auth=self.getAuth())
        self.jobs = [job["name"] for job in r.json()['jobs']]

    def searchJobByName(self, jobname):
        res = process.extractOne(jobname, self.getAllJobs())
        return res[0] if res[1] > 86 else None

    def getJobStatus(self, jobname):
        url = self.jenkins_url + "/job/" + jobname + \
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


# --------------- Tests for job interaction and fuzzy search ------------------
def testJobInteraction(jenkins):
    print(jenkins.getAllJobs())

    r = jenkins.getJobStatus("sleep-test")
    print(r.json())

    # Start the job
    r = jenkins.startJob("sleep-test")
    print(r.text)

    # Get the job status immediately
    r = jenkins.getJobStatus("sleep-test")
    print(r.json())

    # Get it again ten seconds later
    time.sleep(10)
    r = jenkins.getJobStatus("sleep-test")
    print(r.json())

    # Abort the job
    r = jenkins.abortJob("sleep-test")
    print(r.text)

def testFuzzySearch(jenkins):
    print(jenkins.searchJobByName("website build"))
    print(jenkins.searchJobByName("sleeping test"))
    print(jenkins.searchJobByName("sleep test"))

if __name__ == "__main__":
    import time
    jenkins = Jenkins()
    jenkins.readSettingsFromFile()

    testJobInteraction(jenkins)
    testFuzzySearch(jenkins)
