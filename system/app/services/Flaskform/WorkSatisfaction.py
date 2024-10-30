from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired

class WorkSatisfactionForm(FlaskForm):
    Work_Life_Balance = SelectField('Work Life Balance', choices=[('Satisfactory', 'Satisfactory'), ('Unsatisfactory', 'Unsatisfactory')], validators=[DataRequired()])
    Recognition = SelectField('Recognition', choices=[('Satisfactory', 'Satisfactory'), ('Unsatisfactory', 'Unsatisfactory')], validators=[DataRequired()])
    Job_Satisfaction = SelectField('Job Satisfaction', choices=[('Satisfactory', 'Satisfactory'), ('Unsatisfactory', 'Unsatisfactory')], validators=[DataRequired()])
    Company_Satisfaction = SelectField('Company Satisfaction', choices=[('Satisfactory', 'Satisfactory'), ('Unsatisfactory', 'Unsatisfactory')], validators=[DataRequired()])
