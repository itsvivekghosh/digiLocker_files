from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'Secret Key'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Vivek@1999@localhost:3306/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


### Employee Table
class Employee(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	userName = db.Column(db.String(100), unique=True, nullable=False)
	firstName = db.Column(db.String(100), nullable = False)
	lastName = db.Column(db.String(100), nullable = False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(100), unique=True, nullable=False)
	dateOfBirth = db.Column(db.Date(), nullable = False)

	def __init__(self, userName, firstName, lastName, email, phone, dateOfBirth):
		self.userName = userName
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.phone = phone
		self.dateOfBirth = dateOfBirth


@app.route('/')
def index():
	all_data = Employee.query.all()
	return render_template('index.html', employees = all_data)


@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		userName = request.form['userName']
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		email = request.form['email']
		phone = request.form['phone']
		dateOfBirth = request.form['dateOfBirth']

		my_data = Employee(userName, firstName, lastName, email, phone, dateOfBirth)
		db.session.add(my_data)
		db.session.commit()

		flash("Employee Inserted Successfully!", 'success')

		return redirect(url_for('index'))



@app.route('/edit', methods = ['GET', "POST"])
def edit():
	if request.method == 'POST':
		my_data = Employee.query.get(request.form.get('id'))
		my_data.userName = request.form['userName']
		my_data.firstName = request.form['firstName']
		my_data.dateOfBirth = request.form['dateOfBirth']
		my_data.lastName = request.form['lastName']
		my_data.email = request.form['email']
		my_data.phone = request.form['phone']

		db.session.commit()

		flash("Employee Updated Successfully!", 'success')

		return redirect(url_for('index'))


@app.route('/delete/<id>', methods=["GET", "POST"])
def delete(id):
	my_data = Employee.query.get(id)
	db.session.delete(my_data)
	db.session.commit()

	flash("Employee Deleted Successfully!", 'warning')

	return redirect(url_for('index'))



if __name__ == "__main__":
	app.run(debug=True)