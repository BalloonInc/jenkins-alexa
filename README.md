# jenkins-alexa
Use Alexa to trigger Jenkins builds. You can start builds, stop builds, and ask for the status of a build.
You start a job by telling Alexa the jobname, and Alexa will do some fuzzy search in the list of all jobs on your jenkins instance, so you don't need to map any voice input to job names. 


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

## Disclaimer
This project is in an early stage, and works only with a certain setup.

Use the `master` branch if you plan to list all your jenkins jobs as 'slots' in the alexa skill language model. This is possible if you have a limited set of jobs that almost never changes. 

Use the branch `literal` if you add and remove jenkins jobs often. The job names are not known by alexa, and she passes whatever name you give her to our python service, which tries to map it to a correct build. This is less reliable. :warning: Alexa can ask jenkins to do unexpected things.
