from flask import Blueprint, render_template, request, redirect, url_for, session
from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login


alert_blueprint = Blueprint('bp_alerts', __name__)


@alert_blueprint.route('/')
# Include Function Decorator
@requires_login
def index():
    print(f"ALERT BP {session['rks_email']}")
    # alerts_present = Alert.all()
    alerts_present = Alert.find_many_by('user_email', session['rks_email'])
    return render_template('alerts/alert_index.html', alerts=alerts_present)

@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        # process the Data from the Form.
        # access the Item_ID, & Item_Price from the form
        alert_name = request.form['name_of_alert']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])  # Str needs to converted to Float

        store = Store.find_by_url(item_url)

        item = Item(alert_name, item_url, store.tag_name, store.query)
        print(f"ITEM LOAD PRICE::: {item}")
        item.load_price()
        print(f"ITEM PRICE is found = {item.price}")
        print(f"ITEM AFTER PRICE is found ===== {item}")
        print(f"URL = {item_url}")

        my_item = Item.get_by_name(alert_name)
        print(f"FIND ITEM found ===== {my_item}")

        if my_item is None:
            print("SAVING ITEM ::::::::::: INTO MONGO")
            item.save_to_mongo()
        else:
            # assign found item's item._id to be passed to Alert module.
            item._id = my_item._id

        # item.save_to_mongo()

        # The warning below is fine as we are using but not changing the protected variable
        #print(f"Aname: {alert_name}  IT_id = {item._id}  2ndIT_id = {my_item._id}  PRICE = {price_limit}  MAIL: {session['rks_email']}")
        Alert(alert_name, item._id, price_limit, session['rks_email']).save_to_mongo()

    return render_template('alerts/new_alert.html')

@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert_by_id = Alert.get_by_id(alert_id)

    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert_by_id.price_limit = price_limit
        alert_url = alert_by_id.item.url

        # We'l now update the Alert Entry in DB.
        alert_by_id.save_to_mongo()
        # Call below computes the URL to go to index method inside the current blueprint using '.'
        return redirect(url_for('.index'))

    return render_template('alerts/edit_alert.html',alert=alert_by_id)

@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
# No GET or POST method is required as we are not dealing with any form here
def delete_alert(alert_id):
    my_alert = Alert.get_by_id(alert_id)
    if my_alert.user_email == session['rks_email']:
        my_alert.remove_from_mongo()
    return redirect(url_for('.index'))