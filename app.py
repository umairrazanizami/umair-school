from flask import Flask, session, render_template, request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random
import os

# ============ initial configuration + DB configuration==========================


app = Flask(__name__)
app.config["SECRET_KEY"] = "somesecret"

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# db.create_all()

# ======================== DB Models ===============================================

class User(db.Model):

    name = db.Column(db.String(40), unique=True, nullable=False, primary_key = True)
    password = db.Column(db.String(40), unique=False, nullable=False)
    role = db.Column(db.String(40), unique=False, nullable=False)

class Teacher(db.Model):

    name = db.Column(db.String(40), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    qualification = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(13), unique=False, nullable=False)
    role = db.Column(db.String(13), unique=False, nullable=False)


class Student(db.Model):

    name = db.Column(db.String(40), unique=True, nullable=False, primary_key=True)
    parent_name = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(40), unique=False, nullable=False)
    std_class = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    role = db.Column(db.String(13), unique=False, nullable=False)

db.create_all()

# =========================== Routes ==========================================================


@app.route('/')
@app.route('/index')
def home():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect('/admin')
        else:
            return render_template('index.html')
    return redirect('/login')


# ==================== login page ===================================


@app.route('/login')
def login():
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect('/admin')
        else:
            return redirect('/')

    return render_template('login.html')



# ===================== LogIn ==================================================

@app.route('/userLogin', methods=["POST"])
def userLogin():
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if role == 'teacher':
            userFound = Teacher.query.filter_by(name=name, password=password).first()
        elif role == 'student':
            userFound = Student.query.filter_by(name=name, password=password).first()
        else:
            userFound = User.query.filter_by(name = name , password = password).first()


        if userFound:
            session['username'] = name
            session['role'] = role
            # return render_template('index.html')
            loginMsg = "LogIn Successfull"
            success = True
            # session['key_name'] = 'key_value'
            return render_template('loginMsg.html', loginMsg=loginMsg , success = success)
            return redirect('/')
        else:
            loginMsg = "username or password is incorrect , Try Again"
            return render_template('loginMsg.html', loginMsg=loginMsg)
        #
    return render_template('login.html')

# =========================/// LogIn ===============================/////////////


# ============ Admin page ========================================================

@app.route('/admin')
def admin():
    if 'role' in session:
        if session['role'] == 'admin':
            return render_template('adminIndex.html')
        return('/')
    return('/login')

# ============== add Teacher form page ============================

@app.route('/addTeacher')
def addTeacher():
    return render_template('addTeacher.html')

# ----------------- Teacher Added-------------------------------------------------------------------------------


@app.route('/newTeacher' ,  methods=['POST'])
def newTeacher():
    if request.method == 'POST':
        teacher = Teacher()

        teacher.name = request.form['teacherName']
        teacher.role = request.form['role']
        teacher.email = request.form['email']
        teacher.contact = request.form['contact']
        teacher.city = request.form['city']
        teacher.qualification = request.form['qualification']
 # random password ===================================
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        passwordLen = 10
        password = ''.join(random.choices(upper+lower+digits , k = passwordLen))
        teacher.password = str(password)


        db.session.add(teacher)
        db.session.commit()
        signupMsg = "new teacher is added"
        success = True
        return render_template('signupMsg.html',  signupMsg=signupMsg, success=success)

    return '<h1>method not supported</h1>'


# ================ student Add page======================
@app.route('/addStudent')
def addStudent():
    return render_template('addStudent.html')


# --------------------- end of teacher adding ----------------------------/////////////////////////


# --------------------------Student added----------------------------------------------------------------------


@app.route('/newStudent' ,  methods=['POST'])
def newStudent():
    if request.method == 'POST':
        student = Student()

        student.name = request.form['studentName']
        # student.password = request.form['password']
        student.role = request.form['role']
        student.std_class = request.form['stdClass']
        student.contact = request.form['contact']
        student.city = request.form['city']
        student.parent_name = request.form['parent_name']

        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        passwordLen = 10
        password = ''.join(random.choices(upper + lower + digits, k=passwordLen))
        teacher.password = str(password)

        db.session.add(student)
        db.session.commit()

        signupMsg = "new student is added"
        success = True

        return render_template('signupMsg.html', signupMsg=signupMsg, success=success)

    return "<h1>method not supported</h1>"



# -------------- end of student Adding --------------------------------------------------------////////////



# ================ view Teacher for admin =====================================


@app.route('/viewTeacher')
def showTeachers():
    teachers = Teacher.query.all()
    return render_template('showEntries.html' , teachers=teachers , value = 'teacher')


# =============== view students for admin =====================================

@app.route('/viewStudent')
def showStudent():
    students = Student.query.all()
    return render_template('showEntries.html' , students = students ,value = 'student' )


# ======================SignOut============================================

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('role', None)
    session.pop('username', None)
    return redirect('/login')

# ========================== edit teacher ======================

@app.route('/editTeacher')
def editTeachers():
    if 'role' in session:
        if session['role'] == 'admin':
            teachers = Teacher.query.all()
            return render_template('/editEntries.html' , teachers = teachers , value = 'teacher' )
        return redirect('/')
    return redirect('/')

# ================ edit teacher for admin ========================

@app.route('/edit_teacher' , methods = ['POST'])
def editTeacher():
    if request.method == 'POST':
        oldName = request.form['oldName']

        teacher = Teacher.query.filter_by(name = oldName).first()

        teacher.name = request.form['name']
        teacher.email = request.form['email']
        teacher.password = request.form['password']
        teacher.qualification = request.form['qualification']
        teacher.contact = request.form['contact']
        teacher.city = request.form['city']

        db.session.add(teacher)
        db.session.commit()
        return redirect('/editTeacher')

    return redirect('/')

# ==========delete teacher ===================

@app.route('/delete_teacher', methods = ['POST'])
def delete_teacher():
    if request.method == 'POST':
        name = request.form['oldName']

        teacher = Teacher.query.filter_by(name = name).first()
        db.session.delete(teacher)
        db.session.commit()

        return redirect('/editTeacher')

    return redirect('/')

# =============== edit student ===============================

@app.route('/editStudent')
def editStudent():
    if 'role' in session:
        if session['role'] == 'admin':
            students = Student.query.all()
            return render_template('editEntries.html' , students = students , value = 'student' )

# ======================== edit a student ========================================

@app.route('/edit_student' , methods = ['POST'])
def edit_student():
    if request.method == 'POST':
        oldName = request.form['oldName']

        student = Student.query.filter_by(name=oldName).first()

        student.name = request.form['name']
        student.parent_name = request.form['parent']
        student.password = request.form['password']
        student.std_class = request.form['stdclass']
        student.contact = request.form['contact']
        student.city = request.form['city']

        db.session.add(student)
        db.session.commit()
        return redirect('/editStudent')

    return redirect('/')

# =============== delete student ===================

@app.route('/delete_student', methods = ['POST'])
def delete_student():
    if request.method == 'POST':
        name = request.form['oldName']

        student = Student.query.filter_by(name = name).first()
        db.session.delete(student)
        db.session.commit()

        return redirect('/editStudent')

    return redirect('/')



# ----------------------- end of code and app running--------------------------------

app.run(debug=True)