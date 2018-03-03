import requests
import os

class JenkinsSettings:
    def __init__(self, jenkins_url=None, username=None, auth_token=None):
        self.jenkins_url = jenkins_url
        self.username = username
        self.auth_token = auth_token

    def getAuth(self):
        return (self.username, self.auth_token)

def startJob(job, settings):
    url= settings.jenkins_url+'/job/'+job+'%20merge%20master%20to%20staging/build'
    return requests.post(url, auth=settings.getAuth())

def abortJob(job, settings):
    url=""
    return None

def getStatusForJob(job, settings):
    url=""
    return None

def readSettingsFromEnvironment():
    jenkins_url = os.environ["jenkins_url"]
    username = os.environ["jenkins_username"]
    auth_token = os.environ["jenkins_auth_token"]
    return JenkinsSettings(jenkins_url, username, auth_token)

def readSettingsFromFile():
    import yaml
    with open("settings.yaml", 'r') as stream:
        try:
            settings = yaml.load(stream)
            jenkins_url = settings["jenkins_url"]
            username = settings["jenkins_username"]
            auth_token = settings["jenkins_auth_token"]
            return JenkinsSettings(jenkins_url, username, auth_token)
        except yaml.YAMLError as exc:
            print("Could not read settings.yaml") 
            print("Verify if the file exists and has a correct syntax and has all necessary values filled in.")
            print("See settings.yaml.sample for what is needed.")
            print(exc)
            exit()

if __name__ == "__main__":
    settings = readSettingsFromFile()
    startJob("BalloonInc-web", settings)
