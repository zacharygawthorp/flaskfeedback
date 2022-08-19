"""Feecback Flask app."""
from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedBackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "THISISASECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Homepage, redirect to register form."""

    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data 

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username
        
        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form and handle submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username or password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route('/logout')
def logout():
    """logout user."""

    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """Show info about logged in user."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("/users/show.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add feedback form and process."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedBackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.title.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/new.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["POST", "GET"])
def update_feedback(feedback_id):
    """Show update feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedBackForm(obj=feedback)

    if form.validate_on_submit():
        title = form.title.data
        content = form.title.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    
    return redirect(f"/users/{feedback.username}")
