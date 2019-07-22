from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render('')

@app.route("/loggedin", methods=['POST'])
def welcome():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if username == '' or ' ' in username or len(username) < 3 or len(username) > 20 :
        username_error = "Not a valid username"
    if password == '' or ' ' in password or len(password) < 3 or len(password) > 20:
        password_error = "Invalid password"
    if not verify==password:
        verify_error = "Passwords do not match"
    if ' ' in email or not "@" in email or not "." in email or len(email) < 3 or len(email) > 20:
        email_error = "Invalid email"
    if not username_error and not password_error and not verify_error:
        return redirect('/welcome?username={0}'.format(username))
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error) 


@app.route("/welcome")
def success():
    username = request.args.get('username')
    template = jinja_env.get_template('login.html')
    return template.render(name=username)

app.run()