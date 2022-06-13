from pyexpat import features
from django.shortcuts import redirect
from flask import Flask, render_template, request , url_for
import pymongo
from bson.objectid import ObjectId
from pymongo.message import query
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

CAR_PICS_FOLDER = 'static/images/cars/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['CAR_PICS_FOLDER'] = CAR_PICS_FOLDER

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_url)
client.list_database_names()
database_name = "carRental"
db = client[database_name]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about-us")
def about_us():
    return render_template("about-us.html")

@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")

@app.route("/our-services")
def our_services():
    return render_template("our-services.html")

@app.route("/car-list")
def car_list():
    data = db.cars.find()
    lists = []
    for i in data:            
        i.update({"_id": str(i["_id"])})
        lists.append(i)
    return render_template("car-list.html",data=lists)

@app.route("/car/<string:id>")
def car(id):
    data = db.cars.find_one({"_id":ObjectId(id)})
    return render_template("car.html",data=data)

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# admin Dashboard 
@app.route("/admin-dashboard")
def admin_dashboard():
    return render_template("admin_dashboard_index.html")

@app.route("/add-car", methods=['GET','POST'])
def add_car():
    if request.method == 'POST':
        title = request.form.get("title")
        desc = request.form.get("desc")
        per_day = int(request.form.get("per_day"))
        transmission = request.form.get("transmission")
        doors = int(request.form.get("doors"))
        luggages = int(request.form.get("luggages"))
        passengers = int(request.form.get("passengers"))
        # features 
        sunroof = request.form.get('sunroof')
        gps = request.form.get('gps')
        audo_input = request.form.get('audo-input')
        all_wheel = request.form.get('all-wheel')
        bluetooth = request.form.get('bluetooth')
        usb_input = request.form.get('usb-input')
        fm = request.form.get('fm')
        file = request.files['picture']
        if 'picture' not in request.files:
            return "No Picture found"
        if file.filename == '':
            return "No Picture found"
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['CAR_PICS_FOLDER'], filename))

        features = []
        if sunroof == "on":
            features.append("Sunroof")
        if gps == "on":
            features.append("GPS Navigation")
        if audo_input == "on":
            features.append("Audio input")
        if all_wheel == "on":
            features.append("All Wheel drive")
        if bluetooth == "on":
            features.append("Bluetooth")
        if usb_input == "on":
            features.append("USB input")
        if fm == "on":
            features.append("FM Radio")
        # save into database 
        db.cars.insert_one({
            "title":title,
            "transmission":transmission,
            "per_day":per_day,
            "picture":filename,
            "desc":desc,
            "luggages":luggages,  
            "passengers":passengers,  
            "doors":doors,  
            "features":features
        })
        return "True"
    else:
        return render_template("add-car.html")

if __name__ == "__main__":
    app.run(debug=True)