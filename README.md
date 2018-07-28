
# Python script to Lambda function
This is a project that turned the [aquabot Python script](https://github.com/opsdisk/aquabot) into an AWS Lambda function.


# Basic Setup

* CloudWatch Event trigger cron job in UTC: `cron(15 16 * * ? *)` - replaces time.sleep() in a while loop.
* No VPC
* Handler: `aquabot.lambda_handler`
* Role has `AWSLambdaBasicExecutionRole` and `AWSLambdaMicroserviceExecutionRole` policies
* Security Group: Outbound 443 only for data.edwardsaquifer.org and twitter.com
* Test event is an empty dictionary: `{}`
* Can read twitter_creds.json; tested with environment variables and that also worked.


# Install Python modules
## No virtualenv

```bash
cd aquabot_lambda
pip3 install -r requirements.txt -t .
zip -qr9 ../lambdapackage.zip .
```

## virtualenv

* Easiest to create virtual environment in the parent folder of the project
* Then add site-packages directory after initially creating the zip folder

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r aquabot_lambda/requirements.txt
```

```bash
cd aquabot_lambda
zip -qr9 ../lambdapackage.zip .
cd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -qru9 ../../../../lambdapackage.zip .
cd -
deactivate
```