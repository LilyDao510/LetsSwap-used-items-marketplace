from flask import Flask, render_template, request
import os
import util.users as users
import util.items as items
from models import Users, Items, ExchangeRequests, Comments, db
from sqlalchemy.orm import aliased
from flask import Blueprint
from flask_login import login_required, login_user, current_user, logout_user, LoginManager, login_manager
from flask import flash, redirect, url_for
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['TEMPLATES_AUTO_RELOAD']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lien_dao:dummy@localhost/hb_item_exchange'
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
db.init_app(app)

# Google OAuth 2.0 configuration
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'your_redirect_uri'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()

@app.route('/')
def index():
  if current_user.is_authenticated:
    return render_template('home.html')
  else:
    return redirect(url_for('login'))
  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
      address = request.form['address']

      if not users.verify_unique_user(email):
        flash('Email already in use.')
        return redirect(url_for('register'))

      # Generate a password hash
      hashed_password = pbkdf2_sha256.encrypt(password)

      user = Users(name=username, email=email, password=hashed_password, address=address)
      print(user)
      # Add the user to the database
      db.session.add(user)
      db.session.commit()
      
      # Flash a success message to the user
      flash('Account created successfully!')

      return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        print(user)
        if user and pbkdf2_sha256.verify(password, user.password):
            # Login the user
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/explore')
@login_required
def explore():
    user = current_user
    items = get_items_with_owner_id(user.id)
    return render_template('explore.html', user=user, items=items)

@app.route('/profile')
@login_required
def profile():
    user = current_user
    items = get_items_with_owner_id(user.id)
    return render_template('profile.html', user=user, items=items)

@app.route('/logout')
def logout():
  """Logs the user out of the application."""
  logout_user()
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)

@app.route("/users")
def list_users():
    users = Users.query.all()
    return render_template("users.html", users=users)


@app.route("/items")
def list_items():
    items = Items.query.join(Users).add_columns(Items.id,Items.type, Items.condition, Items.status, Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name"), Users.id.label("user_id"), Users.email).all()
    return render_template("index.html", items=items)

#endpoint to list one item by id
@app.route("/items/<int:item_id>")
def get_item(item_id):
    print(item_id)
    item = get_item_with_id(item_id)
    print(item)
    requester_user_id = current_user.get_id()
    if item.owner_id == requester_user_id:
        flash('You cannot exchange your own item')
        return redirect(url_for('list_items'))
    requester_items = get_items_with_owner_id(requester_user_id)
    print("check", requester_items)
    return render_template("item.html", item=item, requester_items=requester_items)

#endpoint to list all item by user_id
@app.route("/users/<int:user_id>/items")
def list_items_by_user(user_id):
    items = get_items_with_owner_id(user_id)
    return render_template("index.html", items=items)
  
#endpoint to list all item by current user
@app.route("/users/items")
def list_items_by_current_user():
    items = get_items_with_owner_id(current_user.get_id())
    return render_template("index.html", items=items)

@app.route("/users/<int:user_id>/items")
def list_items_by_user_id(user_id):
    items = get_items_with_owner_id(user_id)
    return render_template("index.html", items=items)

#endpoin to add a new item
@app.route("/items/create", methods=["GET", "POST"])
def add_item():
    if not current_user.is_authenticated:
        flash('You have to login first to list item for exchange')
        return redirect(url_for('login'))
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        condition = request.form["condition"]
        type = request.form["type"]
        if request.files['image']:
            image_file = request.files["image"]
        image_url = items.upload_image(image_file)
        user_id = current_user.get_id()
        item = Items(name=name, description=description, image_url=image_url, owner_id=user_id, status='ACTIVE', condition=condition, type=type)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('list_items'))
    if request.method == 'GET':
        return render_template('create_item.html')

#endpoint to update an item
@app.route("/items/<int:item_id>/update", methods=["GET", "POST"])
def update_item(item_id):
    item = Items.query.get(item_id)
    if request.method == "POST":
        id = item.id
        name = request.form["name"]
        description = request.form["description"]
        image_url = request.form["image_url"]
        user_id = request.form["user_id"]
        item = Items(name=name, description=description, image_url=image_url, user_id=user_id)
        Items.update(item)
        return render_template("index.html")


#endpoint to create an exchange with a listed item
@app.route("/items/<int:item_id>/exchange", methods=["GET", "POST"])
def exchange_item(item_id=None):
    if not current_user.is_authenticated:
        flash('You have to login first to create exchange request')
        return redirect(url_for('login'))
    if request.method == "POST":
        item_id = item_id
        requester_item_id = request.form["requester_item_id"]
        shipping_type = request.form["shipping_type"]
        address = request.form["address"]
        exchange_request = ExchangeRequests(item_id=item_id, requester_item_id=requester_item_id, shipping_type = shipping_type, address = address, status='PENDING')
        db.session.add(exchange_request)
        db.session.commit()
        return redirect(url_for('list_exchanges', user_id = requester_user_id))
    if request.method == 'GET':
        item = get_item_with_id(item_id)
        requester_user_id = current_user.get_id()
        if item.owner_id == requester_user_id:
            flash('You cannot exchange your own item')
            return redirect(url_for('list_items'))
        requester_items =  get_items_with_owner_id(requester_user_id)
        return render_template('create_exchange_request.html', requester_items = requester_items, item = item)
   
#endpoint to list all exchanges that one user sent or received
@app.route("/users/<int:user_id>/exchanges")
def list_exchanges(user_id):
    items = get_items_with_owner_id(user_id)
    item_ids = []
    for item in items:
        item_ids.append(item.id)
    received_exchanges = ExchangeRequests.query.filter(ExchangeRequests.item_id.in_(item_ids)).all()
    sent_exchanges = ExchangeRequests.query.filter(ExchangeRequests.requester_item_id.in_(item_ids)).all()
    print(received_exchanges)
    print(sent_exchanges)
    return render_template("list_exchanges.html", sent_exchanges=sent_exchanges, received_exchanges=received_exchanges)

@app.route("/exchanges")
def list_my_exchanges():
    user_id = current_user.get_id()
    return redirect(url_for('list_exchanges', user_id = user_id))

#endpoint to list one exchange with exchange_id
@app.route("/exchanges/<int:exchange_id>")
def list_exchange(exchange_id):
    exchange = ExchangeRequests.query.get(exchange_id)
    return render_template("exchange.html", exchange=exchange)

def get_items_with_owner_id(user_id):
    return Users.query.join(Items).add_columns(Items.id,Items.type,Items.condition, Items.status, Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name"), Users.email).\
        filter_by(owner_id=user_id).all()

def get_item_with_id(item_id):
    return Users.query.join(Items).\
        add_columns(Items.id,Items.type,Items.condition, Items.status, Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name"), Users.email).\
        filter_by(id=item_id).first()


#endpoint to accept or reject an exchange request with status param

@app.route("/exchanges/<int:exchange_id>/<status>", methods=["PUT"])
def accept_reject_exchange(exchange_id,status):
    print(exchange_id, status)
    exchange = ExchangeRequests.query.get(exchange_id)
    exchange = ExchangeRequests(exchange.id, status=status)
    ExchangeRequests.update(exchange)
    return redirect(url_for('list_exchanges'))

if __name__ == "__main__":
    app.run(host='0000000', port=5000, debug=True)

