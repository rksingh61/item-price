from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import User, UserErrors

user_blueprint = Blueprint('bp_users', __name__)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():

    if(request.method == 'POST'):
        my_email = request.form['nm_email']
        my_password = request.form['nm_password']

        try:
            User.register_user(my_email, my_password)
            session['rks_email'] = my_email
            return my_email

        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():

    if(request.method == 'POST'):
        my_email = request.form['nm_email']
        my_password = request.form['nm_password']

        try:
            User.is_login_valid(my_email, my_password)
            session['rks_email'] = my_email
            return my_email

        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')

@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login_user'))
