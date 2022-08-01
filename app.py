from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:kifadmin@localhost:5434/rental_tracker"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

all_properties = []

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250), unique=True, nullable=False)
    tenant_name = db.Column(db.String(250))

    def __init__(self, address, tenant_name):
        self.address = address
        self.tenant_name = tenant_name

    def __repr__(self):
        return f"<Property {self.address}>"


@app.route('/')
def home():
    all_properties = Property.query.all()
    #return render_template("index.html", properties=all_properties)
    return render_template("index.html", properties=all_properties)


@app.route('/properties', methods=['POST', 'GET'])
def handle_properties():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_property = Property(address=data['address'], tenant_name=data['tenant_name'])
            db.session.add(new_property)
            db.session.commit()
            return {"message": f"property {new_property.address} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    
    elif request.method == 'GET':
        properties = Property.query.all()
        results = [
            {
                "id": property.id,
                "address": property.address,
                "tenant_name": property.tenant_name
            } for property in properties
        ]

        return {"count": len(results), "properties": results}


@app.route('/add_property', methods=['GET','POST'])
def add_property():
    if request.method == "POST":
        #CREATE RECORD
        new_property = Property(
            address=request.form["address"],
            tenant_name=request.form["tenant_name"]
        )
        db.session.add(new_property)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_property.html")

@app.route('/edit_tenant', methods=['GET', "POST"])
def edit_tenant():
    if request.method == "POST":
        #UPDATE TENANT
        property_id = request.form["id"]
        property_to_update = Property.query.get(property_id)
        property_to_update.tenant_name = request.form["tenant_name"]
        db.session.commit()
        return redirect(url_for('home'))
    property_id = request.args.get('id')
    property_selected = Property.query.get(property_id)
    return render_template("edit_tenant.html", property=property_selected)

@app.route('/edit_address', methods=['GET', "POST"])
def edit_address():
    if request.method == "POST":
        #UPDATE ADDRESS
        property_id = request.form["id"]
        property_to_update = Property.query.get(property_id)
        property_to_update.address = request.form["address"]
        db.session.commit()
        return redirect(url_for('home'))
    property_id = request.args.get('id')
    property_selected = Property.query.get(property_id)
    return render_template("edit_address.html", property=property_selected)

@app.route('/delete_property', methods=['GET'] )
def delete_property():
    if request.method == 'GET':
        property_id = request.args.get('id')
        property_to_delete = Property.query.get(property_id)
        db.session.delete(property_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)