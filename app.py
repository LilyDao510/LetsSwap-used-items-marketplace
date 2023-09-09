from flask import Flask, render_template, request
import os
import util.users
from models import Users, Items, ExchangeRequests, Comments, db
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lien_dao:dummy@localhost/hb_item_exchange'
db.init_app(app)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('profile.html', name=current_user.name)
    else:
        return render_template('login.html')

@app.route("/users")
def list_users():
    users = Users.query.all()
    return render_template("users.html", users=users)


@app.route("/items")
def list_items():
    items = Items.query.join(Users).add_columns(Items.name,Items.description, Items.image_url, Users.name.label("user_name"), Users.id.label("user_id"), Users.email).all()
    return render_template("index.html", items=items)

#endpoint to list one item by id
@app.route("/items/<int:item_id>")
def list_item(item_id):
    item = Items.query.get(item_id)
    return render_template("item.html", item=item)

#endpoin to add a new item
@app.route("/items/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        image_url = request.form["image_url"]
        user_id = request.form["user_id"]
        item = Items(name=name, description=description, image_url=image_url, user_id=user_id)
        Items.add_item(item)
        return render_template("index.html")
    else:
        return render_template("item_form.html")

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


@app.route('/item/<int:item_id>/upload-image', methods=['POST'])
def upload_image():
    """Upload an image file to Google Cloud Storage."""

    # Get the image file from the request.
    image = request.files['image']

    # Get the file name and encode it.
    filename = image.filename
    encoded_filename = filename.encode('utf-8')

    # Upload the image to Google Cloud Storage.
    bucket = storage.Bucket('my-bucket')
    blob = bucket.blob(encoded_filename)
    blob.upload_from_file(image)

    # Return the success message.
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(host='0000000', port=5000, debug=True)

