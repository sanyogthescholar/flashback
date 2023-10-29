from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('index.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def save_uploaded_file():
   if request.method == 'POST':
      f = request.files['file']
      try:
        f.save(os.path.join(app.instance_path, request.form['name'], secure_filename(f.filename))) #https://stackoverflow.com/a/42425388/13681680
      except FileNotFoundError: #the directory doesn't exist
         os.makedirs("uploaded_files/" + str(request.form['name']), exist_ok=True) #create directory and typecast to string for safety.Also https://stackoverflow.com/a/273227/13681680
         f.save(os.path.join("uploaded_files", request.form['name'], secure_filename(f.filename)))
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)