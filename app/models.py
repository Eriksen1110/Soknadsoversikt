from flask_sqlalchemy import SQLAlchemy
import datetime
from uuid import uuid4
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt() 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), 
                   primary_key=True, 
                   default=lambda: uuid4().hex)
    email = db.Column(db.String(120), 
                      unique=True, 
                      nullable=False)
    name = db.Column(db.String(100), 
                     nullable=False)
    password_hash = db.Column(db.String(128), 
                              nullable=False)
    date_created = db.Column(db.DateTime, 
                             default=datetime.datetime.now)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.String(32), 
                   primary_key=True, 
                   default=lambda: uuid4().hex)
    name = db.Column(db.String(100), 
                     unique=True, 
                     nullable=False)
    industry = db.Column(db.String(100))
    website = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, 
                             default=datetime.datetime.now)

    def __init__(self, name, industry=None, website=None):
        self.name = name
        self.industry = industry
        self.website = website

    def __repr__(self):
        return f"<Company {self.name}>"

class Application(db.Model):
    id = db.Column(db.String(32), 
                   primary_key=True)
    role = db.Column(db.String(100), 
                     nullable=False)
    category = db.Column(db.String(100), 
                         nullable=False)
    deadline = db.Column(db.Date, 
                         nullable=False)
    status = db.Column(db.String(50), 
                       nullable=False)
    link = db.Column(db.String(255))
    date_created = db.Column(db.Date, 
                             default=datetime.datetime.now)
    user_id = db.Column(db.String(32),
                        db.ForeignKey(User.id),
                        nullable=False)
    company_id = db.Column(db.String(32), 
                           db.ForeignKey(Company.id),
                           nullable=False)
                        
    company = db.relationship('Company', backref='applications')
    user = db.relationship('User', backref='applications')

    def __init__(self, role, category, deadline, status, link, user_id, company_id):
        self.id = uuid4().hex
        self.role = role
        self.category = category
        self.deadline = deadline
        self.status = status
        self.link = link
        self.user_id = user_id
        self.company_id = company_id

    def days_left(self):
        """Calculate the number of days left until the deadline."""
        return (self.deadline - datetime.date.today()).days

    def to_json(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "category": self.category,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "link": self.link,
            "date_created": self.date_created.strftime("%Y-%m-%d"),
            "days_left": self.days_left()
        }


class StatusChange(db.Model):
    __tablename__ = 'status_changes'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(32), db.ForeignKey('application.id'), nullable=False)
    old_status = db.Column(db.String(50), nullable=True)
    new_status = db.Column(db.String(50), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.datetime.now)

    application = db.relationship('Application', backref='status_changes')

    def __init__(self, application_id, old_status, new_status):
        self.application_id = application_id
        self.old_status = old_status
        self.new_status = new_status
