from flask import Flask ,jsonify, make_response,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from sqlalchemy import or_,and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1:5432/test'
db = SQLAlchemy(app)

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'no': obj.no,
                'userType': obj.userType,
                'age': obj.age,
                'password': obj.password,
                'bgType': obj.bgType,
                'rhValue': obj.rhValue,
            }
        return super(MyJSONEncoder, self).default(obj)

app.json_encoder = MyJSONEncoder


class User(db.Model):
    __tablename__ = 'bank'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    no = db.Column(db.Integer )
    userType = db.Column(db.Boolean)
    age = db.Column(db.String(120))
    password = db.Column(db.String(120))
    bgType = db.Column(db.String(2))
    rhValue = db.Column(db.Boolean)

    def __init__(self,name,email,no,userType,age,password,bgType,rhValue):
        # self.id  = id
        self.name  = name
        self.email  = email
        self.no  = no
        self.userType  = userType
        self.age  = age
        self.password  = password
        self.bgType  = bgType
        self.rhValue  = rhValue

    def __init__(self,data):
        self.name = data['name']
        self.email = data['email']
        self.no = int(data['no'])
        self.userType = data['userType']
        self.age = int(data['age'])
        self.password = data['password']
        self.bgType = data['bgType']
        self.rhValue = data['rhValue']


    def __repr__(self):
        return  '<User %r>' % self.name







# db.create_all()

# user = User('zubair','zub@g.com',1123123,True,22,123,True,True)
# db.session.add(user)
# db.session.commit()

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    if len(User.query.filter_by(email=email).all()) == 0:
            user = User(request.form)
            db.session.add(user)
            db.session.commit()
            return jsonify({'data': user, 'message': 'Sucessfully Registered', 'error': ''})
    return jsonify({'data': '', 'message': 'Failed', 'error': 'User with ' + email + ' Already registered'})


@app.route('/login', methods = ['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameters'})
    else:
        # return jsonify(User.query.filter_by(email=email, password=password).all())
        user = User.query.filter_by(email=email, password=password).all()
        if len(user) != 0:
            user = user[0]
            # return jsonify(user.userType)
            if user.userType == True:
                filtered = filteredBloodGroupForRecipient(user.bgType, user.rhValue)
                return jsonify({'data': {'user': user, 'recipients': filtered.all()},
                                 'message': 'Sucessfully Login', 'error': ''})
            filtered = filteredBloodGroupForDonar(user.bgType, user.rhValue)
            return jsonify(
                {'data': {'user': user, 'donars': filtered.all()}, 'message': 'Sucessfully Login',
                 'error': ''})

        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid email/Password'})


@app.route('/getAllUsers/<int:id>/')
def getAll(id):
    try:
        id = id
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id)
        if user is None:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
            filtered = User.query.filter(User.id!=id)
            return jsonify({'data': {'user': user.all(), 'All': filtered.all()},'message': 'Sucessfull', 'error': ''})


@app.route('/getAllDonars/<int:id>/')
def getAllDonars(id):
    try:
         id = id
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id)
        if user is None:
           return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
           filtered = User.query.filter_by(userType=False)
           return jsonify({'data': {'user': user.all(), 'donars': filtered.all()},'message': 'Sucessfull', 'error': ''})


@app.route('/getAllRecipients/<int:id>/')
def getAllRecipients(id):
    try:
         id = id
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id)
        if user is None:
           return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
           filtered = User.query.filter_by(userType=True)
           return jsonify({'data': {'user': user.all(), 'Recipients': filtered.all()},'message': 'Sucessfull', 'error': ''})





@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Notfound' }),404)


if __name__ == '__main__':
    app.run(debug=True)
# userType == False is Donar and other is Recipient


def filteredBloodGroupForRecipient(bgType,rhValue=False):
    print('reci='+bgType)
    if rhValue == False:
        print('this is here')
        if bgType.lower() == 'a':
           return  User.query.filter_by(userType=False).filter(or_(User.bgType=='C', User.bgType=='A')).filter_by(rhValue=False)
        elif bgType.lower() == 'b':
            return User.query.filter_by(userType=False).filter(or_(User.bgType == 'C', User.bgType == 'B')).filter_by(rhValue=False)
        elif bgType.lower() == 'c':
            return User.query.filter_by(userType=False,bgType='C').filter_by(rhValue=False)
        elif bgType.lower() == 'ab':
            return User.query.filter_by(userType=False).filter_by(rhValue=False)
        else:
            return "Error"
    else:
        if bgType.lower() == 'a':
            print('A')

            return User.query.filter_by(userType=False).filter( or_(User.bgType=='C', User.bgType=='A'))
        elif bgType.lower() == 'b':
            print('B')

            return  User.query.filter_by(userType=False).filter(or_(User.bgType == 'C', User.bgType == 'B'))
        elif bgType.lower() == 'c':
            print('C')

            return  User.query.filter_by(userType=False,bgType='C')
        elif bgType.lower() == 'ab':
            print('AB')

            return User.query.filter_by(userType=False)
        else:
            return "Error"


def filteredBloodGroupForDonar(bgType,rhValue=False):
    print('Donar='+bgType)
    if rhValue == False:
        if bgType.lower() == 'a':
           return  User.query.filter_by(userType=True).filter(or_(User.bgType=='AB', User.bgType=='A'))
        elif bgType.lower() == 'b':
            return User.query.filter_by(userType=True).filter(or_(User.bgType=='AB', User.bgType=='B'))
        elif bgType.lower() == 'c':
            return User.query.filter_by(userType=True)
        elif bgType.lower() == 'ab':
            return User.query.filter_by(userType=True,bgType='AB')
        else:
            return "Error"
    else:
        if bgType.lower() == 'a':
           return  User.query.filter_by(userType=True).filter(or_(User.bgType=='AB', User.bgType=='A')).filter_by(rhValue=True)
        elif bgType.lower() == 'b':
            return User.query.filter_by(userType=True).filter(or_(User.bgType=='AB', User.bgType=='B')).filter_by(rhValue=True)
        elif bgType.lower() == 'c':
            return User.query.filter_by(userType=True).filter_by(rhValue=True)
        elif bgType.lower() == 'ab':
            return User.query.filter_by(userType=True,bgType='AB').filter_by(rhValue=True)
        else:
            return "Error"