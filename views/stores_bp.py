import json
from flask import Blueprint, render_template, request, redirect, url_for
from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login, requires_admin

store_blueprint = Blueprint('bp_stores', __name__)


@store_blueprint.route('/')
@requires_login
def index():
    stores_present = Store.all()
    print("RKS: STORE INDEX ALL done")
    return render_template('stores/store_index.html', stores=stores_present)

@store_blueprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def new_store():
    if request.method == 'POST':
        # process the Data from the Form.
        # access the Item_ID, & Item_Price from the form
        store_name = request.form['name_of_store']
        url_prefix = request.form['nm_url_prefix']
        tag_name = request.form['name_tag']
        query = json.loads(request.form['nm_query'])

        Store(store_name, url_prefix, tag_name, query).save_to_mongo()

    return render_template('stores/new_store.html')



@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store_by_id = Store.get_by_id(store_id)

    if request.method == 'POST':
        store_name = request.form['name_of_store']
        url_prefix = request.form['nm_url_prefix']
        tag_name = request.form['name_tag']
        query = json.loads(request.form['nm_query'])

        # Modify the Store object
        store_by_id.store_name = store_name
        store_by_id.url_prefix = url_prefix
        store_by_id.tag_name = tag_name
        store_by_id.query = query

        # We'll now update the Store Entry in DB.
        store_by_id.save_to_mongo()
        # Call below computes the URL to go to index method inside the current blueprint using '.'
        return redirect(url_for('.index'))

    # somehow if we do not use Dumps below, the Query gets passed to HTML as '' single quotes
    # this then is discarded by json.loads().
    my_query = store_by_id.query
    store_by_id.query = json.dumps(my_query)

    return render_template('stores/edit_store.html',store=store_by_id)

@store_blueprint.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('.index'))

