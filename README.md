# Serverless Mailer

Serverless mailer written in Flask, uses Mailgun to deliver contact emails.

The endpoint expects a POST with the following required form parameters:

- name - The name of the sender.
- email - The email of the sender.
- message - The message sent by the sender.
- redirect - The URL to redirect to after sending the email.

An example HTML form is included to test your implementation. Change the form action and the redirect value before testing.

## Requirements

- AWS account.
- AWS CLI with configured credentials.
- Serverless CLI.
- Mailgun account.

## AWS Lambda deployment

Define required parameters in Systems Manager Parameter Store:

    aws ssm put-parameter --name mailerTo --type String --value admin@example.com
    aws ssm put-parameter --name mailgunDomain --type String --value mailer.example.com
    aws ssm put-parameter --name mailgunKey --type String --value key-12345678901234567890

Optionally specify the subject:

    aws ssm put-parameter --name mailerSubject --type String --value 'Website contact!'

To deploy to AWS Lambda:

    sls deploy

The parameters are used at _deploy time_. If you make a change to any of the parameters, you must redeploy the function.

If you have not defined the _mailerSubject_ parameter, you will see a warning during deploy which can be ignored.

## Local development

Copy example and edit:

    cp .env.example .env
    vim .env (or nano .env)

Setup environment:

    mkvirtualenv -r requirements.txt serverless-mailer

To run server:

    python app.py
