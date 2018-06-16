from flask import Flask , render_template , session , request , url_for , redirect
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'try_app_users'
app.config['MONGO_URI'] = 'mongodb://kunnu:khiladi1@ds259620.mlab.com:59620/try_app_users'

mongo  = PyMongo(app)

@app.route('/loginSuccessful')
def login_success():
	if 'username' in session:
		return  'successfully logged in as' +session['username']
	else:
		return 'Username Not Stored in the Session'



@app.route('/', methods = ['GET','POST'])
def index():
 #this part considers that the user has already been registered thus it queries the database for existing user
        if 'username' in session:
                return  'successfully logged in as' +session['username']
        if request.method == 'POST':
                print('Catch POST Request')
                #query part
                users = mongo.db.users
                #function to find a particular query
                login_user = users.find_one({'name':request.form['username']})
                if login_user == True:
                        if bcrypt.hashpw(request.form['pass'].encode('utf-8'),login_user['password'].encode('utf-8') == login_user['password'].encode('utf-8')):
                                session['username'] = request.form['username']
                                return redirect(url_for('login_success'))
                        else:
                                return 'failed'
                else:
                        return'Invalid username/password'
        elif request.method == 'GET':
                return render_template('html_for_app.html')


@app.route('/register.html',methods = ['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')


	elif request.method == 'POST':
		print('Catch POST Request for Signup')
		users = mongo.db.users
		existing_user = users.find_one({'name' : request.form['username']})
		if existing_user :
			return 'Sorry ! The username already exists!!!!'
		else:
			hashPass = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt()) #creating hashed password and also salting it
			#inserting the login credentials into the database
			users.insert({'name' : request.form['username'] , 'password' : hashPass})
			session['username'] == request.form['username']
			return redirect(url_for('login_success'))





if __name__ == '__main__':
	app.secret_key  = "kunalIsAwesome"
	app.run(debug = True)
