import os
#from methods import File_handler
import joblib
from loguru import logger
from random import choice, randint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import Flask, flash, session, render_template, request, url_for, send_file

app = Flask(__name__)

app.config['SECRET_KEY'] = "this_is_my_secret_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ewd_user:MountainFire2022@localhost/Content'#"sqlite:///Content.db"

db = SQLAlchemy(app)
model =joblib.load('model & Pipeline/Classifier.pkl')
pipeline = joblib.load('model & Pipeline/pipeline.pkl')
#-----------------------------------------------------------------------
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email  = db.Column(db.String(50))
    password  = db.Column(db.String(50))

class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(50))
    email  = db.Column(db.String(50))
    employer  = db.Column(db.String(50))
    dependants = db.Column(db.Integer)
    claims = db.Column(db.Integer)
    period = db.Column(db.Integer)

class Claims(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    member_name  = db.Column(db.String(50))
    patience_name  = db.Column(db.String(50))
    email  = db.Column(db.String(50))
    location  = db.Column(db.String(50))
    gender  = db.Column(db.String(50))
    dob  = db.Column(db.String(50))
    cause  = db.Column(db.String(50))
    employer  = db.Column(db.String(50))
    relationship = db.Column(db.String(50))
    patient_suffix = db.Column(db.Integer)
    dependants = db.Column(db.Integer)
    fee_charged = db.Column(db.Integer)
    label = db.Column(db.Integer)
    claims = db.Column(db.Integer)
    period = db.Column(db.Integer)
    status = db.Column(db.String(50))

#-----------------------------------------------------------------------

@app.route('/', methods = ['POST','GET'])
def sign_in():
    if request.method == 'POST':
        email = request.form['Email']
        password =  request.form['Password']
        admin = Users.query.filter_by(email =email,password=password).first()
        if admin != None:
            return upload()
        
    return render_template('Account/account.html')

@app.route('/upload', methods = ['POST','GET'])
def upload():
    template = 'Account/manage/upload.html'
    return render_template(template)


@app.route('/evaluate', methods = ['POST','GET'])
def evaluate():
    if request.method == 'POST':
        state = choice([0,0,1])
        score = randint(30,65)
        session['eva'] =[state, score, 89]
        
        claim = Claims(
            member_name  = request.form['member_name'],
            patience_name = request.form['patient_name'],
            email = request.form['email'],
            location = request.form['location'],
            gender = request.form['gender'],
            dob = request.form['patient_dob'],
            cause = request.form['cause'],
            employer = request.form['employer'],
            relationship = request.form['relationship'],
            patient_suffix = request.form['patient_suffix'],
            dependants = request.form['number_of_dependants'],
            fee_charged = request.form['Fee_Charged'],
            period = request.form['membership_period'],
            claims = request.form['number_of_claims'],
            label = state,
        )
        db.session.add(claim)
        db.session.commit()
        logger.sucess('data saved!')
        
        return view()
    template = 'Account/manage/upload.html'
    return render_template(template)

@app.route('/view')
def view():
    data = Claims.query.order_by(Claims.id.desc()).first()
    logger.info(data)
    template = 'Account/manage/viewContent.html'
    
    return render_template(template,eva=session['eva'], data=data)


@app.route('/blacklist')
def blacklist():
    data = Claims.query.filter_by(status = 'blacklisted').all()
    template = 'Account/Manage/blacklist.html'
    
    return render_template(template,data=data)

@app.route('/claim')
def claim():
    data = Claims.query.all()
    template = 'Account/manage/claims.html'
    
    return render_template(template,data=data)


@app.route('/details/<int:id>')
def details(id):
    data = Claims.query.filter_by(id = id).first()
    template = 'Account/manage/details.html'
    
    return render_template(template,data=data)


@app.route('/action/<string:act>/<int:id>')
def action(act, id):
    claim_update =  Claims.query.filter_by(id = id).first()
    db.session.add(claim_update)
    db.session.commit()
    if act == 'block':
        claim_update.status = 'Blocked'
        db.session.add(claim_update)
        db.session.commit()
        return claim()
    elif act == 'approve':
        claim_update.status = 'Approved'
        db.session.add(claim_update)
        db.session.commit()
        return claim()
    elif act== 'blacklist':
        claim_update =  Claims.query.filter_by(id = id).first()
        claim_update.status = 'Blacklisted'
        db.session.add(claim_update)
        db.session.commit()
        return blacklist()
        
    
    return upload()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('Misc/not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')
