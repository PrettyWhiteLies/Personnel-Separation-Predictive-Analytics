from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, DecimalField
from wtforms.validators import DataRequired,NumberRange

class PersonalForm(FlaskForm):
    Gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    Age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=16, max=100)])
    Relationship_Status = SelectField('Relationship Status', choices=[('Single', 'Single'), ('Married', 'Married'), ('De-facto', 'De-facto'), ('Divorced', 'Divorced')], validators=[DataRequired()])
