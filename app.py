import os
import requests

from dotenv import load_dotenv
from flask import abort, Flask, jsonify, render_template, redirect, request

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    for param in ['name', 'email', 'message', 'redirect']:
        if param not in request.form:
            abort(400, '%s is a required parameter' % param)

    text = f'''
Hi there,

You have a received a website contact:

Name: {request.form['name']}
Email: {request.form['email']}

{request.form['message']}

Regards,
Mailer
'''

    data = {
        'from': '%s <%s>' % (request.form['name'], request.form['email']),
        'to': os.getenv('MAILER_TO'),
        'subject': os.getenv('MAILER_SUBJECT', 'Website contact'),
        'text': text,
    }

    requests.post(
        'https://api.mailgun.net/v3/%s/messages' % os.getenv('MAILGUN_DOMAIN'),
        auth=('api', os.getenv('MAILGUN_KEY')),
        data=data
    )

    return redirect(request.form['redirect'])

if __name__ == "__main__":
    app.run()
