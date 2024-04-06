from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
# we must instatiate bcrypt

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key = True)
    password = db.Column(db.Text, nullable= False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
    # when you use cascade="all,delete", you are specifying that
    #  all changes made to the parent object (User in this case) 
    # should cascade to the related objects (Feedback in this case), 
    # and if the parent object is deleted, all related objects
    # should also be deleted automatically. This helps maintain
    # data integrity and ensures that related records are
    # handled appropriately when the parent record is modified or removed.
    # start of convenience class methods

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # the flask bcrypt version allows us to generate hashed pw without first getting own salt
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name,email=email)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

   

    
    
def connect_db(app):
    db.app = app
    db.init_app(app)
