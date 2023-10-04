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
    return redirect(url_for('list_items'))
  else:
    return redirect(url_for('login'))
  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
      if not users.verify_unique_user(email):
        flash('Email already in use.')
        return redirect(url_for('register'))

      # Generate a password hash
      salt = os.urandom(64)
      hashed_password = pbkdf2_sha256.encrypt(password)

      user = Users(name=username, email=email, password=hashed_password, salt="dummy")
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


@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)

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
    items = Items.query.join(Users).add_columns(Items.id,Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name"), Users.id.label("user_id"), Users.email).all()
    return render_template("index.html", items=items)

#endpoint to list one item by id
@app.route("/items/<int:item_id>")
def list_item(item_id):
    item = Items.query.join(Users).add_columns(Items.id,Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name")).filter_by(id=item_id).first()
    return render_template("item.html", item=item)

#endpoint to list all item by user_id
@app.route("/users/<int:user_id>/items")
def list_items_by_user(user_id):
    items = Users.query.join(Items).add_columns(Items.id,Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name"), Users.id.label("user_id"), Users.email).filter_by(owner_id=user_id).all()
    return render_template("index.html", items=items)
  
#endpoint to list all item by current user
@app.route("/users/<int:user_id>/items")
@app.route("/users/items")
def list_items_by_current_user():
    items = Users.query.join(Items).add_columns(Items.id, Items.name,Items.owner_id, Items.description, Items.image_url, Users.name.label("user_name"), Users.id.label("user_id"), Users.email).filter_by(owner_id=user_id).all()
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
        #TODO upload to google cloud storage
        if request.files['image']:
            image_file = request.form["image"]
        image_url = items.generate_unique_file_name()
        user_id = current_user.get_id()
        item = Items(name=name, description=description, image_url=image_url, owner_id=user_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
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
@app.route("/items/<int:item_id>/exchange")
@app.route("/exchange_requests/create")
def exchange_item(item_id=None):
    if not current_user.is_authenticated:
        flash('You have to login first to create exchange request')
        return redirect(url_for('login'))
    if request.method == "POST":
        item_id = request.form["item_id"]
        address = request.form["address"]
        requester_item_id = request.form["requester_item_id"]
        shipping_type = request.form["shipping_type"]
        exchange_request = ExchangeRequests(item_id=item_id, requester_item_id=requester_item_id, shipping_type = shipping_type, address = address)
        db.session.add(exchange_request)
        db.session.commit()
        return render_template("list_exchanges.html")
    if request.method == 'GET':
        requester_user_id = current_user.get_id()
        requester_items =  Users.query.join(Items).add_columns(Items.id, Items.name,Items.owner_id).filter_by(owner_id=requester_user_id).all()
        print(requester_items)
        return render_template('create_exchange_request.html')
   

if __name__ == "__main__":
    app.run(host='0000000', port=5000, debug=True)

