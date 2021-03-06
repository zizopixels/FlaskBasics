"""
This will contain all the functions and views related to user authentication
"""

from functools import wraps

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, abort)
from flask_bcrypt import check_password_hash, generate_password_hash

import db

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get("username", None)
        if not username:
            return redirect(url_for('auth.login', next=request.url))
        g.user = db.get_user(username)
        if g.user is None:
            return redirect(url_for('auth.login', next=request.url))

        db_conn = db.get_database_connection()

        with db_conn.cursor() as cursor:
            sql = ("SELECT"
                        " belongs_to.slug, project.project_id, organisation.name"
                    " FROM"
                        " `user`"
                    " LEFT OUTER JOIN"
                        " belongs_to ON user.username = belongs_to.username"
                    " LEFT OUTER JOIN"
                        " project ON project.slug = belongs_to.slug"
                    " LEFT OUTER JOIN"
                        " organisation ON organisation.slug = belongs_to.slug"
                    " WHERE"
                        " user.username = %s;")
            cursor.execute(sql, (username, ))
            result = cursor.fetchall()
            g.user["orgs"] = {}
            g.orgs = {}

            if result is not None:
                for record in result:
                    organisation_slug = record["slug"]
                    project_id = record["project_id"]
                    org_data = g.orgs.get(organisation_slug, None) or {"name": record["name"]}
                    l = org_data.get("projects", None) or []
                    org_data["projects"] = l + [project_id]
                    g.orgs[organisation_slug] = org_data

        return f(*args, **kwargs)
    return decorated_function



def check_valid_org_and_project(f):
    """
    Used to restrict access to URLs based on the user.
    Returns 404 if it not a valid page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            # This shouldn't happen, all the endpoints using this decorator must use login_required
            # But just in case.
            return redirect(url_for('auth.login', next=request.url))
        organisation = request.view_args.get('organisation', None) or request.view_args.get('slug', None)
        project_id = request.view_args.get('project_id', None)

        if organisation in g.orgs:
            if project_id is not None and project_id not in g.orgs[organisation]["projects"]:
                # Valid org but invalid project
                abort(404)
        else:
            # Not a valid project
            abort(404)
    
        return f(*args, **kwargs)
    return decorated_function

@blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        user = check_user_login(username, password)
        if not user:
            flash("Invalid username or password", "danger")
            return render_template('login.html', next=request.args.get("next", None))
        else:
            session["username"] = user["username"]
            if request.args.get('next', None):
                return redirect(request.args["next"])
            return redirect(url_for('organisation.organisation'))

@blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

@blueprint.route('/me', methods=["GET"])
@login_required
def my_details():
    return g.user or {}


def get_email(email):
    db_conn = db.get_database_connection()
    with db_conn.cursor() as cursor:
        sql = 'SELECT `email` FROM `user` WHERE `email`=%s'
        cursor.execute(sql, (email, ))
        result = cursor.fetchone()
        return result

def check_user_login(username: str, password: str):
    if username and password:
        result = db.get_user(username, with_password=True)
        if result:  
            return result if check_password_hash(result["password"], password) else None 
    return None



@blueprint.route('/signup',methods=["GET","POST"])
def signup():
    if 'username' in session:
        return redirect(url_for('auth.my_details'))
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        username = request.form.get("username", None)
        first_name = request.form.get("first_name", None)
        last_name = request.form.get("last_name", None)
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        print(f'{username}')

        if username and first_name and last_name and email and password:
            user = db.get_user(username)
            if user is not None:
                flash("Username already exists","danger")
                return render_template('signup.html')
            else:
                _email = get_email(email)
                if _email is not None:
                    flash("Email already exists","danger")
                    return render_template('signup.html')
                else:
                    password_hash = generate_password_hash(password)
                    db_conn = db.get_database_connection()                
                    with db_conn.cursor() as cursor:
                        cursor.execute("INSERT INTO `user`(`username`,`email`,`first_name`,`last_name`,`password`) Values (%s, %s, %s, %s, %s)", (username, email, first_name, last_name, password_hash))
                        db_conn.commit();
                    session["username"] = username
                    return redirect(url_for('organisation.organisation'))
        else:
            if not username:
                flash("Enter Username", "danger")
            if not first_name:
                flash("Enter First name", "danger")
            if not last_name:
                flash("Enter Last name", "danger")
            if not email:
                flash("Enter Email", "danger")
            if not password:
                flash("Enter Password", "danger")
            
            return render_template('signup.html')