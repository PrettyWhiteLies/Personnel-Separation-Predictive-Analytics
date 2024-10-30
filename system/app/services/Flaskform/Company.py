from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired

class CompanyForm(FlaskForm):
    Employee_Department = SelectField('Employee Department', choices=[('Operations', 'Operations'), ('Management', 'Management'), ('HR', 'HR'), ('Finance', 'Finance'), ('Technical', 'Technical')], validators=[DataRequired()])
    Years_in_Current_Role = IntegerField('Years in Current Role', validators=[DataRequired()])
    Years_with_Current_Supervisor = IntegerField('Years with Current Supervisor', validators=[DataRequired()])
    Years_Since_Last_Promotion = IntegerField('Years Since Last Promotion', validators=[DataRequired()])
    Percentage_Increase_in_Salary = DecimalField('Percentage Increase in Salary', places=2, validators=[DataRequired()])
