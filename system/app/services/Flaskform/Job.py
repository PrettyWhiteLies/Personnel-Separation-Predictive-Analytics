from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired
class JobForm(FlaskForm):
    Position_Role = StringField('Position Role', validators=[DataRequired()])
    Job_Type = SelectField('Job Type', choices=[('Permanent', 'Permanent'), ('Fixed-term', 'Fixed-term'), ('Contract', 'Contract'), ('Casual', 'Casual')], validators=[DataRequired()])
    Job_Location = SelectField('Job Location', choices=[('On-Site', 'On-Site'), ('Remote', 'Remote'), ('Hybrid', 'Hybrid')], validators=[DataRequired()])
    Seniority_Level = SelectField('Seniority Level', choices=[('Graduate', 'Graduate'), ('Junior', 'Junior'), ('Mid', 'Mid'), ('Senior', 'Senior'), ('Executive', 'Executive')], validators=[DataRequired()])
    Salary_Band = DecimalField('Salary Band', places=2, validators=[DataRequired()])
    Hours_Worked_Per_Week = DecimalField('Hours Worked Per Week', places=2, validators=[DataRequired()])
    Value_of_Benefits = DecimalField('Value of Benefits', places=2, validators=[DataRequired()])
    performance_rating = SelectField('Performance Rating', choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], validators=[DataRequired()])
    Training_Opportunities = SelectField('Training Opportunities', choices=[('Satisfactory', 'Satisfactory'), ('Unsatisfactory', 'Unsatisfactory')], validators=[DataRequired()])
    Travel_Percentage = DecimalField('Travel Percentage', places=2, validators=[DataRequired()])
    Unpaid_Overtime_Percentage = DecimalField('Unpaid Overtime Percentage', places=2, validators=[DataRequired()])
