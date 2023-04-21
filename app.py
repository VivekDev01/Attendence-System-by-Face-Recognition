from flask import Flask,render_template,request,redirect,url_for,session,Response
from flask_mysqldb  import MySQL
import MySQLdb.cursors
import pickle
import cv2
import os
from keras_facenet import FaceNet
from mtcnn.mtcnn import MTCNN
import numpy as np
import mysql.connector as db_connector
from datetime import date,time
from face import Embeddings
from werkzeug.utils import secure_filename

my_db = db_connector.connect(host = "localhost",user = "ankit",passwd = "deeplearning",
database = "iitranchi_attendence_system",auth_plugin="mysql_native_password",autocommit = True)
my_cursor = my_db.cursor()

file = open("encoded_data.p","rb")
face_embeddings = pickle.load(file)

app = Flask(__name__,template_folder="template") 
app.secret_key = os.urandom(22)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 

streaming= True

def mark_attendence(id,name):
    try:
        current_day = date.today()
        my_cursor.execute("insert into attendence values(%s , %s, %s);",(id,name,current_day))
    except:
        return 
    
def video_streaming():
    face_encoder = FaceNet()
    face_detector = MTCNN()
    global capture
    url = "http://100.90.209.161:8080/video"
    capture = cv2.VideoCapture(0)
    while streaming:
        isTrue,image = capture.read()
        if not isTrue:
            continue
        try:
            img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            bbox = face_detector.detect_faces(img)[0]["box"]
            x,y,w,h = bbox
            x1,y1,x2,y2 = x,y,x+w,y+h
            face = img[y1:y2,x1:x2]
            face = face.reshape(1,face.shape[0],face.shape[1],face.shape[2])
            embeddings = face_encoder.embeddings(face)
            student_id = []
            distance = []
            for id,vector in face_embeddings.items():
                student_id.append(id)
                distance.append(face_encoder.compute_distance(embeddings[0],vector[0]))
            print(distance)
            if(distance[np.argmin(distance)] < 0.3):
                id = student_id[np.argmin(distance)]
                my_cursor.execute("select student_name from students where student_id = %s",(id,))
                name = my_cursor.fetchone()[0]
                cv2.rectangle(image,(x1,y1),(x2,y2),(255,0,0),3)
                cv2.putText(image,name,(x1,y1),cv2.FONT_HERSHEY_TRIPLEX,2,(255, 255, 255))
                mark_attendence(id,name)
            else:
                msg = "Student Not Present in DataBase!"
                cv2.putText(image,msg,(15,460),cv2.FONT_HERSHEY_TRIPLEX,1,(255, 255, 255))
            cv2.resize(image,(224,224))
            ret,buffer = cv2.imencode(".jpg",image,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')      
        except:
            msg = "No One Detected!"
            cv2.resize(image,(224,224))
            cv2.putText(image,msg,(150,460),cv2.FONT_HERSHEY_TRIPLEX,1,(255, 255, 255))
            ret,buffer = cv2.imencode(".jpg",image,[int(cv2.IMWRITE_JPEG_QUALITY), 50])
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')  
            continue
    capture.release()
    cv2.destroyAllWindows()

@app.route('/')
def landing_page():
    return render_template('login_page.html')

@app.route("/home")
def home():
    return render_template("home_page.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    user_name = "as0287519@gmail.com"
    pass_word = "nidhi_kuswaha"
    if(request.method == "POST" and "username" in request.form and "password" in request.form):
        username = request.form["username"]
        password = str(request.form["password"])
        if username == user_name and password == pass_word:
            session["loggedin"] = True
            session["username"] = username
            session["id"] = username
            return redirect("/home")
    else:
        return render_template('login_page.html')
    
@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop("udername",None)
    session.pop("id",None)
    return render_template('login_page.html')

@app.route('/take_attendence',methods = ["POST"])
def take_attendence():
    return render_template('attendence.html')

@app.route('/attendence')
def attendence():
    return Response(video_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stopcamera', methods=["GET",'POST'])
def stopcamera(): 
    capture.release()
    cv2.destroyAllWindows()
    return redirect("/home")

@app.route('/add')
def add():
    return render_template('new_student.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/new_registration',methods = ["GET","POST"])
def new_registration():
    if (request.method == "POST" and "student_name" in request.form and "roll_no" in request.form and "semester" in request.form 
    and "image" in request.files):
        name = request.form["student_name"]
        roll = request.form["roll_no"]
        semester = request.form["semester"]
        image = request.files["image"]
        img_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        img_file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        embeddings = Embeddings()
        embeddings.adding_new_face(img_file_path,roll)
        my_cursor.execute('insert into students values(%s,%s,%s)',(roll,name,semester))
        msg = 'new student is registered successfully!'
        return redirect("/home")
    return redirect("/home")
    

@app.route("/students_information",methods = ["POST"])
def students_information():
    if (request.method == "POST" and "date" in request.form):
        date = request.form["date"]
        my_cursor.execute("select student_id from attendence where in_time = %s",(date,))
        ids = my_cursor.fetchall()
        student_ids = [ids[i][0] for i in range(len(ids))]
        students_name = []
        for i in range(len(ids)):
            my_cursor.execute("select student_name from students where student_id = %s",(student_ids[i],))
            student_name = my_cursor.fetchone()[0]
            students_name.append(student_name)
        students_semester = []
        for i in range(len(ids)):
            my_cursor.execute("select semester from students where student_id = %s",(student_ids[i],))
            semester = my_cursor.fetchone()[0]
            students_semester.append(semester)
        length = len(student_ids)
        return render_template("post_information_last.html",student_ids = student_ids,students_name =students_name,students_semester = students_semester,length = length,date = date)
    if request.method == 'POST' and "roll_no" in request.form:
        try:
            student_id = request.form["roll_no"]
            my_cursor.execute("select count(in_time) from attendence where student_id = %s",(student_id,))
            class_attended = my_cursor.fetchone()[0]
            info = dict()
            my_cursor.execute("select student_name from students where student_id = %s",(student_id,))
            name = my_cursor.fetchone()[0]
            info["student_id"] = student_id
            info["class_attended"] = class_attended
            info["student_name"] = name 
            return render_template("/post_information.html",info = info)
        except:
            return render_template("/post_information.html",msg= "Student is not in database!")
    else:
        return redirect("/home")



if __name__ == '__main__':
    app.run(debug=True)

