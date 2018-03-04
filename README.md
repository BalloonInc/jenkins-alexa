# jenkins-alexa
Use Alexa to trigger Jenkins builds.

## Requirements
- An [Amazon development account](https://developer.amazon.com) (free to register)
- An [Amazon AWS account](https://console.aws.amazon.com) (I think this is also free)
- Amazon echo family device, or home made alternative (raspberry pi + alexa)
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