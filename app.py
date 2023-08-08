from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import pandas as pd

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://if0_34777426:lp8U5Fgq5fQOodw@sql110.infinityfree.com/if0_34777426_placement1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Marshmallow for serialization
ma = Marshmallow(app)

# Define Company model
class Company(db.Model):
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    total_employees = db.Column(db.Integer)
    total_departments = db.Column(db.Integer, primary_key=True)

# Define Company schema for serialization
class CompanySchema(ma.Schema):
    class Meta:
        fields = ('company_name', 'location', 'total_employees', 'total_departments')

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

# Define Employee model
class Employee(db.Model):
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    department_id = db.Column(db.Integer, primary_key=True)

# Define Employee schema for serialization
class VPEmployeeSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'age', 'salary', 'department_id')

vpemployee_schema = VPEmployeeSchema()
vpemployees_schema = VPEmployeeSchema(many=True)

# Route to fetch all employee data
@app.route('/alldata', methods=['GET'])
def get_employees():
    try:
        all_employees = Alldata.query.all()
        result = employees_schema.dump(all_employees)
        return {"employees": result}, 200
    except Exception as e:
        return {"message": str(e)}, 500

# Route to upload and process company data
@app.route('/company', methods=['POST'])
def upload_company_data():
    try:
        file = request.files['file']
        df = pd.read_excel(file)

        # Create tables if they don't exist
        db.create_all()

        # Prepare and insert company data
        company_data = df.rename(columns={'COMPANY_NAME': 'company_name', 'LOCATION': 'location',
                                         'TOTAL_EMPLOYEES': 'total_employees', 'TOTAL_DEPARTMENTS': 'total_departments'}).to_dict(orient='records')
        db.session.bulk_insert_mappings(Company, company_data)
        db.session.commit()

        return {"message": "Company data inserted successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 500

# Route to fetch all company data
@app.route('/company', methods=['GET'])
def get_companies():
    try:
        all_companies = Company.query.all()
        result = companies_schema.dump(all_companies)
        return {"companies": result}, 200
    except Exception as e:
        return {"message": str(e)}, 500

# Route to upload and process VP employee data
@app.route('/vpemployee', methods=['POST'])
def upload_vpemployee_data():
    try:
        file = request.files['file']
        df = pd.read_excel(file)

        # Create tables if they don't exist
        db.create_all()

        # Prepare and insert VP employee data
        vpemployee_data = df.rename(columns={'FIRST_NAME': 'first_name', 'LAST_NAME': 'last_name',
                                            'AGE': 'age', 'SALARY': 'salary', 'DEPARTMENT_ID': 'department_id'}).to_dict(orient='records')
        db.session.bulk_insert_mappings(Employee, vpemployee_data)
        db.session.commit()

        return {"message": "VP employee data inserted successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 500

# Route to fetch all VP employee data
@app.route('/vpemployee', methods=['GET'])
def get_vpemployees():
    try:
        all_vpemployees = Employee.query.all()
        result = vpemployees_schema.dump(all_vpemployees)
        return {"vpemployees": result}, 200
    except Exception as e:
        return {"message": str(e)}, 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)