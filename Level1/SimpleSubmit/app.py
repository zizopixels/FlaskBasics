from flask import Flask, render_template, request, session, flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml
from pathlib import Path
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)



my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'db.yaml'
#YAML stands for Yet Another Markup Language
#These files are used to store configuration information in our case we have stored DB config

# open db.yaml using yaml module
db = yaml.full_load(open(config_path))
# instantiate an object for the MySQL module
mysql = MySQL(app)

# Configure the db
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		try:
			name = request.form['uname']
			age = request.form['uage']

			# create a cursor by executing cursor function of db object
			cur = mysql.connection.cursor()

			query = "SELECT * FROM employee WHERE name='" + name + "'"
			# take cursor object and call execute function to execute query
			count = cur.execute(query)
			
			if count > 0:
				flash('That name already exists <br> Choose another one', 'warning')
			else:
				cur.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))

				# commit the changes to the database
				mysql.connection.commit()

				# display the success message
				flash('Successfully added the details', 'success')

				# cleanup
				cur.close()
		except:
			flash('Failed to add details', 'danger')
		
	return render_template("index.html", title="Home")


@app.route('/employees')
def employees():
	cur = mysql.connection.cursor()
	count = cur.execute("SELECT * FROM employee")
	
	if count > 0:
		employees = cur.fetchall()
	else:
		employees = None
		flash('Currently no employees in the list', 'secondary')
		
	cur.close()
	return render_template("employees.html", title="Employees", employees=employees)

if __name__ == '__main__':
	app.run(debug=True)
	