from flask import Flask,render_template,Response,request,redirect,flash,jsonify
import pymongo
from bson.objectid import ObjectId
import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.json_encoder = MyEncoder

try:
	mongo = pymongo.MongoClient(host="localhost",port=27017)
	db = mongo.company
	mongo.server_info() # trigger exception if can not connect to db
except:
	print("ERROR - Cannot connect to db")


@app.route('/')
def home():
	users = db.user.find()
	return render_template('home.html',user=users)

@app.route('/users',methods=["POST"])
def create_user():
	if request.method == 'POST':
		eid = request.form.get('eid')
		name = request.form.get('fname')
		email = request.form.get('email')
		password = request.form.get('pass')
	try:
		# print(type(eid))
		if not eid:
			user = {"name" : f"{name}","email":f"{email}","password":f'{password}'}
			dbResponse = db.user.insert_one(user)
			flash("Data Successfully Submited... ",category='success')
			return redirect('/')
		else:
			uemp = db.user.update_one({"_id":ObjectId(eid)}, {"$set":{"name":name,"email":email,"password":password}})
			flash("Data Successfully Updated... ",category='success')
			return redirect('/')	
	except Exception as e:
		flash(f"{e}",category='error')
	return redirect('/')


@app.route('/delete',methods=['POST'])
def Edelete():
	if request.method == 'POST':
		eid = str(request.form.get('eid'))
		# print(eid)
		emp = db.user.delete_one({'_id':ObjectId(eid)})
		return jsonify({'status':1})

	return jsonify({'status':0})

@app.route('/edit',methods=['POST'])
def Eedit():
	if request.method == 'POST':
		eid = request.form.get('eid')
		# print(eid)
		emp = db.user.find_one({'_id':ObjectId(eid)})
		# print(emp['_id'])
		employee = {'id':emp['_id'],'name':emp['name'],'email':emp['email'],'password':emp['password']}
		return jsonify({'status':1,'employee':employee})
	return jsonify({'status':0})




if __name__ == '__main__':
	app.run(debug=True)