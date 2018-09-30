# Serverless Mailer

Serverless mailer written in Flask, uses Mailgun to deliver contact emails.

## Requirements

- AWS account.
- AWS CLI with configured credentials.
- Serverless CLI.
- Mailgun account.

## Form Parameters

The endpoint expects a POST with the following required form parameters:

- name - The name of the sender.
- email - The email of the sender.
- message - The message sent by the sender.
- redirect - The URL to redirect to after sending the email.

## AWS Lambda deployment

Define required parameters in Systems Manager Parameter Store:

    aws ssm put-parameter --name mailerTo --type String --value admin@example.com
    aws ssm put-parameter --name mailgunDomain --type String --value mailer.example.com
    aws ssm put-parameter --name mailgunKey --type String --value key-12345678901234567890

Optional parameters:

    aws ssm put-parameter --name mailerSubject --type String --value 'Website contact!'

To enable support for reCAPTCHA (recommended):

    aws ssm put-parameter --name recaptchaEnabled --type String --value true
    aws ssm put-parameter --name recaptchaSecretKey --type String --value 1234567890bcdefghijkl

To deploy to AWS Lambda:

    sls plugin install -n serverless-python-requirements
    sls plugin install -n serverless-wsgi
    sls deploy

The parameters are used at _deploy time_. If you make a change to any of the parameters, you must redeploy the function.

If you have not defined the _mailerSubject_ parameter, you will see a warning during deploy which can be ignored.

## Local development

Setup some environment variables:

    cp .env.example .env
    vim .env (or nano .env)

Setup Python virtual environment:

    mkvirtualenv -r requirements.txt serverless-mailer

Run server:

    python app.py

## Example Form

An example HTML form is included to test your implementation. It requires you to setup some parameters in _parameters.json_:

    cp parameters.json.example parameters.json

reCAPTCHA must be hosted on a site, the easiest way to serve the folder for local testing is:

    python3 -m http.server

And open (http://localhost:8000/example.html) with your browser.

_NB_: Make sure that the _recaptchaEnabled_ flag matches in _.env_ and _parameters.json_.
