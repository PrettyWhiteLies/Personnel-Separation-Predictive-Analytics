from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired
class QualificationsExperienceForm(FlaskForm):
    Highest_Educational_Qualification = SelectField('Highest Educational Qualification', choices=[('School', 'School'), ('Undergraduate', 'Undergraduate'), ('Post-graduate', 'Post-graduate'), ('Doctorate', 'Doctorate')], validators=[DataRequired()])
    Field_of_Education = SelectField('Field of Education', choices=[('Business', 'Business'), ('Technical', 'Technical'), ('Finance', 'Finance'), ('Arts', 'Arts'), ('Sciences', 'Sciences')], validators=[DataRequired()])
    Years_of_Working_Experience = IntegerField('Years of Working Experience', validators=[DataRequired()])
    Years_within_Current_Domain = IntegerField('Years within Current Domain', validators=[DataRequired()])
