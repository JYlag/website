from app import db
from hashutils import make_pw_hash

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    pw_hash = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

    def __repr__(self):
        return '<User &r' % self.username

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(48))
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    image_path = db.Column(db.String(100))

    def __init__(self, title, summary, description, image_path, date):
        self.title = title
        self.summary = summary
        self.description = description
        self.date = date
        self.image_path = image_path

    def __repr__(self):
        return '<Title &r' & self.title

