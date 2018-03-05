# jenkins-alexa
Use Alexa to trigger Jenkins builds. You can start builds, stop builds, and ask for the status of a build.
You start a job by telling Alexa the jobname, and Alexa will do some fuzzy search in the list of all jobs on your jenkins instance, so you don't need to map any voice input to job names. 


## Sample utterances
You can start jenkins with
> Alexa, start jenkins.

Then ask me to interact with a job:
> Alexa, start build {release}
> Alexa, cancel {deployment to beta}
> Alexa, what is the status of the job {merge master to beta}

You can also avoid the two commands, by instructing Alexa to go and ask Jenkins directly:
> Alexa, ask jenkins what the status is for {continuous build}
d
## Requirements
- A running jenkins instance, and an account (username+API token) that has permissions to start and stop jobs.
- Amazon echo family device, or home made alternative (raspberry pi + alexa)
- An [Amazon development account](https://developer.amazon.com) (free to register)
- An [Amazon AWS account](https://console.aws.amazon.com) (I think this is also free)
- Python 3 and pip installed on your pc

## How to use

1. Install all python packages locally (necessary for Amazon lambda's) 
```
pip install -r requirements.txt -t .
```

2. Create an Amazon lambda in Python 3.

3. Create a zip of the content of this folder (Python files + libraries)

4. Upload the zip file as content of the lambda.

5. Set `jenkins_url`, `jenkins_username` and `jenkins_token` environment variables in the lambda settings.

5. Create an Amazon Alexa skill.

6. Use language-model.json as language model. Don't forget to build it.

7. Set the created Lambda as endpoint for the alexa skill.

If your echo is linked with the same account as your development account, you should be able to test on your device already.

## For developing
- for using `jenkins.py` locally, rename settings.yaml.sample to settings.yaml, and update it with your jenkins url and authentication parameters.
- all `print` statements are written to Amazon's CloudWatch logging. This is very convenient.
- You can test your lambda with test events. This way you don't need to use a voice controlled device all the time.
- Setting `should_end_session` in the intents (`lambda_function.py`) ensures your echo session never closes, which is nice for testing purposes.
