from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time', validators=[DataRequired()])
    close_time = StringField('Closing Time', validators=[DataRequired()])
    Coffee = SelectField('Coffee Rating', validators=[DataRequired()],
                         choices=[('✘', '✘')] + [('☕' * i, '☕' * i) for i in range(1, 6)])
    wifi = SelectField('Wifi Strength Rating', validators=[DataRequired()],
                       choices=[('✘', '✘')] + [('💪' * i, '💪' * i) for i in range(1, 6)])
    power = SelectField('Power Socket Availability', validators=[DataRequired()],
                        choices=[('✘', '✘')] + [('🔌' * i, '🔌' * i) for i in range(1, 6)])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        data_list = list(form.data.values())
        actual_data = data_list[:-2]  # Gets rid of the button value and CSRF Token
        with open('cafe-data.csv', 'a', encoding='utf-8', newline='') as file:
            file.write(','.join(actual_data) + '\n')
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


# TODO: Finish the task by adding the add_cafe route
@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
