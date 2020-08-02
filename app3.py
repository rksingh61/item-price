from flask import Flask, render_template
from views.alerts_bp import alert_blueprint
from views.stores_bp import  store_blueprint
from views.users_bp import  user_blueprint
import os
from libs.mailgun import Mailgun
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = os.urandom(64)
length = len(app.secret_key)

app.config.update(ADMIN=os.environ.get('ADMIN'))

load_dotenv()

# print(os.environ)

print(Mailgun.send_email(
    ['rks@ampool.io'],
    'Hello',
    'This is a Test Message',
    '<p> This is HTML Test </p>'
))

if __name__ == '__main__':
    app.run(debug=True)

