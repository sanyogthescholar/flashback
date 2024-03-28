from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import chromadb
from pymongo import MongoClient
import urllib
import shutil
import io
import base64
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
chroma_client = chromadb.PersistentClient(path="chromadb")
collection = chroma_client.get_collection(name="my_collection")

@app.route('/')
def upload_file():
   return render_template('index.html')

"""Debug Routes for testing"""
"""DO NOT USE IN PRODUCTION"""
@app.route('/delete', methods = ['GET', 'POST'])
def delete():
   collection.delete(collection.get()['ids'])
   return {"status": "success"}

#get all the documents in the collection
@app.route('/getall', methods = ['GET'])
def get():
    return {"documents": collection.get()}

#create a route to delete all folders inside the uploaded_files directory
@app.route('/reset', methods = ['GET'])
def delete_all():
      for root, dirs, files in os.walk("uploaded_files"):
         for d in dirs:
               shutil.rmtree(root+"\\"+d)
      return {"status": "success"}
"""End of Debug Routes"""

#create a route for searching in chromadb using plaintext
@app.route('/search', methods = ['GET'])
def search():
    #search with GET method using the search parameter from the URL
   if request.method == 'GET':
      query = request.args.get('search')
      results = collection.query(
            query_texts=[query],
            n_results=10
        )
        #return in JSON
      return {"results": results}

def get_database():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   user = urllib.parse.quote(os.environ.get('MONGO_USER'))
   password = urllib.parse.quote(os.environ.get('MONGO_PASSWORD'))
   CONNECTION_STRING = f"mongodb+srv://{user}:{password}@cluster0.fkwx6.mongodb.net/flashback"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['flashback']

@app.route('/uploader', methods = ['GET', 'POST'])
def save_uploaded_file():
   if request.method == 'POST':
      files = request.files.getlist('file')
      for f in files:
         try:
            f.save(os.path.join(app.instance_path, request.form['name'], secure_filename(f.filename))) #https://stackoverflow.com/a/42425388/13681680
         except FileNotFoundError: #the directory doesn't exist
            os.makedirs("uploaded_files/" + str(request.form['name']), exist_ok=True) #create directory and typecast to string for safety.Also https://stackoverflow.com/a/273227/13681680
            f.save(os.path.join("uploaded_files", request.form['name'], secure_filename(f.filename)))
         #insert the file into the database
            collection = get_database()['flashback_db']
            file = {
               "name": f.filename,
               "path": os.path.join("uploaded_files", request.form['name'], secure_filename(f.filename)),
               "owner": request.form['name']
            }
            collection.insert_one(file)
      return 'file uploaded successfully'

#https://stackoverflow.com/a/64067673/13681680
"""def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, "JPEG") # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img"""

def get_response_image(image_path):
    img = open(image_path, mode='rb') # reads the PIL image
    print(image_path)
    byte_arr = img.read()
    encoded_img = base64.encodebytes(byte_arr).decode('utf-8') # encode as base64
    return encoded_img

#create an endpoint to get all the files uploaded by a specific user
@app.route('/getfiles', methods = ['GET'])
def get_files():
   name = request.args.get('name')
   files = []
   for root, dirs, filenames in os.walk(f"uploaded_files/{name}"):
      for file in filenames:
         files.append(f"uploaded_files/{name}/" + file)
   #return {"files": files}
   #return render_template('my_files.html', files=files)
   encoded_imges = []
   for image_path in files:
      encoded_imges.append((get_response_image(image_path)))
   return jsonify({'result': encoded_imges})
   #return encoded_imges[0]

if __name__ == '__main__':
   app.run(debug = True)