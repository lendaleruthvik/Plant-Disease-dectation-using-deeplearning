

import os

import numpy as np

# Keras

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
# Flask utils
from flask import Flask, redirect, url_for, request, render_template

import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'



model_path2 = 'models/inceptionresnetv2.h5' # load .h5 Model

CTS = load_model(model_path2, custom_objects={'f1_score': f1_score, 'recall_m': recall_score, 'precision_m': precision_score})


def model_predict2(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(224,224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
      
    
    if result == 0:
        return "Apricot monilia laxa (disease) Detected","after.html"        
    elif result == 1:
        return "Cherry myzus cerasi (disease) Detected","after.html"
    elif result == 2:
        return "Coryneum beijerinckii (disease) Detected", "after.html"
    elif result == 3:
        return "Erwinia amylovora (pest) Detected", "after.html"
    elif result == 4:
        return "Peach monilia laxa (disease)", "after.html"
    elif result == 5:
        return "Peach sphaerolecanium prunastri (pest)", "after.html"
    elif result == 6:
        return "Walnut leaf mite ga (pest)", "after.html"
    elif result == 7:
        return "Xanthomonas arboricola (disease)", "after.html"
    
    
    
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict2',methods=['GET','POST'])
def predict2():
    print("Entered")
    
    print("Entered here")
    file = request.files['files'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
        
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    print("@@ Predicting class......")
    pred, output_page = model_predict2(file_path,CTS)
              
    return render_template(output_page, pred_output = pred, img_src=UPLOAD_FOLDER + file.filename)




@app.route('/notebook')
def notebook():
	return render_template('NOtebook.html')


if __name__ == '__main__':
    app.run(debug=False)