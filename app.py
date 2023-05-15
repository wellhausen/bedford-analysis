from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.static_folder = 'static'

# Set a secret key for form CSRF protection
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/static/css/styles.css')
def serve_css():
    return app.send_static_file('css/styles.css')


# file - file upload input
# submit - form submission button
# DataRequired - ensures the field is not empty
class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        # handle the file upload and data processing
        print("form validated")
    return render_template('../templates/index.html', form=form)