import os
import requests

from asbool import asbool
from dotenv import load_dotenv
from flask import abort, Flask, jsonify, render_template, redirect, request

RECAPTCHA_ERRORS = {
    'missing-input-secret': 'The secret parameter is missing',
    'invalid-input-secret': 'The secret parameter is invalid or malformed.',
    'missing-input-response': 'The response parameter is missing.',
    'invalid-input-response': 'The response parameter is invalid or malformed.',
    'bad-request': 'The request is invalid or malformed.',
}

def get_remoteip():
    trusted_proxies = {'127.0.0.1'}  # define your own set
    route = request.access_route + [request.remote_addr]
    return next((addr for addr in reversed(route)
                 if addr not in trusted_proxies), request.remote_addr)

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    required_params = ['name', 'email', 'message', 'redirect']

    recaptcha_enabled = asbool(os.getenv('RECAPTCHA_ENABLED'))

    if recaptcha_enabled:
        required_params.append('g-recaptcha-response')

    for param in required_params:
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

    if recaptcha_enabled:
        remoteip = get_remoteip()
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': os.getenv('RECAPTCHA_SECRET_KEY'),
                'remoteip': remoteip,
                'response': request.form['g-recaptcha-response'],
            }
        )

        response.raise_for_status()

        data = response.json()

        if not data['success']:
            errors = [RECAPTCHA_ERRORS[errorCode] for errorCode in data['error-codes']]
            abort(400, 'reCAPTCHA: %s' % ', '.join(errors))

    data = {
        'from': '%s <%s>' % (request.form['name'], request.form['email']),
        'to': os.getenv('MAILER_TO'),
        'subject': os.getenv('MAILER_SUBJECT', 'Website contact'),
        'text': text,
    }

    response = requests.post(
        'https://api.mailgun.net/v3/%s/messages' % os.getenv('MAILGUN_DOMAIN'),
        auth=('api', os.getenv('MAILGUN_KEY')),
        data=data
    )

    response.raise_for_status()

    return redirect(request.form['redirect'])

if __name__ == "__main__":
    app.run()
