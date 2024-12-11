from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app and CORS for handling React requests
app = Flask(__name__)
CORS(app, origins="http://localhost:3000")  # Allow cross-origin requests from the frontend (React on localhost:3000)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ConVox%404@172.16.13.29:3306/employee_management_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Employee model (similar to the Employee entity in Spring Boot)
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Employee {self.id}>'
@app.route('/')
def home():
    return "Welcome to the Home Page"

# Routes (similar to the Spring Boot controller)
@app.route('/api/v1/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    result = []
    for emp in employees:
        result.append({
            'id': emp.id,
            'first_name': emp.first_name,
            'last_name': emp.last_name,
            'email': emp.email
        })
    return jsonify(result)

@app.route('/api/v1/employees', methods=['POST'])
def create_employee():
    employee = request.get_json()
    new_employee = Employee(
        first_name=employee['first_name'],
        last_name=employee['last_name'],
        email=employee['email']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({
        'id': new_employee.id,
        'first_name': new_employee.first_name,
        'last_name': new_employee.last_name,
        'email': new_employee.email
    }), 201

@app.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email
    })

@app.route('/api/v1/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    employee = Employee.query.get_or_404(id)

    # Update employee data
    employee.first_name = data['first_name']
    employee.last_name = data['last_name']
    employee.email = data['email']
    db.session.commit()

    return jsonify({
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email
    })

@app.route('/api/v1/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return Response(status=204)

if __name__ == '__main__':
    # Run the Flask app on port 9090
    app.run(host='0.0.0.0', port=9090, debug=True)
