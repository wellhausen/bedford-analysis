from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import math

app = Flask(__name__)
app.static_folder = 'static'

# Set a secret key for form CSRF protection
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/static/css/styles.css')
def serve_css():
    return app.send_static_file('css/tailwind.css')


# file - file upload input
# submit - form submission button
# DataRequired - ensures the field is not empty
class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Submit')

def is_bedford_law_valid(observed_percentages):
    print("observed_percentages::::", observed_percentages)
    expected_percentages = np.array([0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046])
    print("len(expected_percentages)", len(expected_percentages))
    tolerance = 0.01
    
    observed_percentages_rounded = np.round(observed_percentages, 2)
    print("observed_percentages_rounded", len(observed_percentages_rounded))
    diff = np.abs(observed_percentages_rounded - expected_percentages)
    within_range = np.logical_and(diff >= -tolerance, diff <= tolerance)
    valid_bedford = np.all(within_range)
    return valid_bedford


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        df = pd.read_csv(file, sep='\t')

        # Extract the first digit from each number
        data = df['7_2009'].astype(str).str[0]
        
        digit_counts = data.value_counts().sort_index()

        # Calculate the count of each digit
        # if 0 not in digit_counts.index:
        #     digit_counts = pd.concat([digit_counts, pd.Series(0, index=[0])])


        x = list(range(1, 10))

        total_count = digit_counts.sum()
        percentages = digit_counts / total_count * 100
        print("percentages::::", percentages)

        digit_labels = [str(i) for i in x]

        # Create a Plotly figure
        trace = go.Bar(
            x=x,
            y=percentages,
            name='Observed Distribution',
            marker=dict(color='blue'),
            text=percentages.round(2),
            textposition='auto'
        )

        data = [trace]

        layout = go.Layout(
            title='Observed Distribution',
            xaxis=dict(
                title='First Digit Percentage Totals',
                tickmode='array',
                tickvals=x,
                ticktext=digit_labels
            ),
            yaxis=dict(
                autorange=True,
                showticklabels=False
            ),
            width=800,
            height=600
        )

        fig = go.Figure(data=data, layout=layout)

        # Generate HTML code for the plotly graph
        plot_html = fig.to_html(full_html=False, default_width='100%', default_height='100%')

        # Validate Bedford's Law
        valid_bedford = is_bedford_law_valid(percentages)
        print("valid_bedford", valid_bedford)

        return render_template('index.html', form=form, plot_html=plot_html, valid_bedford=valid_bedford)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
