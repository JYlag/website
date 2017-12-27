from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Post, User
from hashutils import check_pw_hash, make_pw_hash
import datetime

app.secret_key = "a1hf892fHre2dsa92J"

def input_is_valid(text):
    return len(text) >= 3 and len(text) <= 20

def verify_passwords(password,verify_pass):
    return password == verify_pass

def get_posts():
    return Post.query.all()

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', posts=get_posts())

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/signup", methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:

            if not input_is_valid(username):
                flash("Username does not meet requirements. Please enter a different user", "error")
            if not input_is_valid(password):
                flash("Password does not meet requirements. Please try again.", "error")
            if not verify_passwords(password,verify):
                flash("Passwords do not match. Please try again.", "error")

            if input_is_valid(username) and input_is_valid(password) and verify_passwords(password,verify):
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/portfolio')
        else:
            flash("Username already exists! Enter a different username", "error")
            return redirect("/signup")


    return render_template("signup.html")

@app.route("/add-post", methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        body = request.form['body']
        img_path = request.form['img']

        new_post = Post(title,summary,body, img_path, date=datetime.datetime.now())
        db.session.add(new_post)
        db.session.commit()
        return redirect("/portfolio")


    return render_template("add-post.html")

@app.route("/logout")
def logout():
    del session['username']
    flash("Bye Joe!")
    return redirect("/admin")

@app.route('/admin', methods=['POST', 'GET'])
def admin():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash("Welcome Joe!")
            return redirect('/portfolio')
        else:
            flash("You've entered an invalid username or password", "error")
            return redirect("/admin")
    return render_template('admin.html')

if __name__ == '__main__':
    app.run()
