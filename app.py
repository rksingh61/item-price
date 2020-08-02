from flask import Flask, render_template
from views.alerts_bp import alert_blueprint
from views.stores_bp import  store_blueprint
from views.users_bp import  user_blueprint
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)
length = len(app.secret_key)

app.config.update(ADMIN=os.environ.get('ADMIN'))

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(user_blueprint, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)

