from flask import Flask,render_template,request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('mongo_uri')
app = Flask(__name__)
client = MongoClient(MONGO_URI,serverSelectionTimeoutMS=5000)


db = client.test
collection = db['flask-app']

@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signuppage():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    # Error 1: empty fields -> same page, no redirect
    if not name or not email:
        return render_template('signup.html', error='Name and email are required.')

    # Error 2: database problem -> same page, no redirect
    try:
        collection.insert_one({'name': name, 'email': email})
    except PyMongoError as e:
        return render_template('signup.html', error=f'Database error: {e}')

    form_data= dict(request.form)
    collection.insert_one(form_data)
    return 'data written sucessfully'

    data = collection.find()

    data = list(data)
    for item in data:
        print(item)

        del item['_id']

    data = {
        'data':data
    }
    return data

if __name__ == '__main__':
    app.run(debug=True)