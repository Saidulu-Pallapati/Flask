from flask import Flask, jsonify, redirect, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ConVox%404@172.16.13.29:3306/agents_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
@app.before_request
def create_tables():
    db.create_all()
db = SQLAlchemy(app)
class Employee(db.Model):
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False)
 

    def __repr__(self):
        return f'<Employee {self.id}>'



@app.route("/add")
def add():
    return render_template("AddEmployee.html")
@app.route('/', methods=['POST','GET','DELETE'])
def index():
    
    employees = Employee.query.all()
    
   
    return render_template("index.html", employees=employees)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    employee = Employee.query.filter_by(id=id).first()
    if not employee:
        return "Employee not found", 404
    if request.method == "POST":
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.phone_number = request.form['phone_number']
        db.session.commit()       
        return redirect('/')  
    return render_template("UpdateEmployee.html", employee=employee)
@app.route("/delete/<int:id>")
def delete(id):
    employee=Employee.query.filter_by(id=id).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")


@app.route('/insert', methods=['POST','GET'])
def create_employee():
    if request.method == "POST":
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')

        if not name or not phone_number or not email:
            
            return "All fields are required", 400

        new_employee = Employee(
            name=name,
            phone_number=phone_number,
            email=email
        )
        db.session.add(new_employee)
        db.session.commit()

        return redirect("/")




if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=9090, debug=True,threaded=True)
