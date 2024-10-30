from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from sqlalchemy.exc import SQLAlchemyError

from ..services.utils.db_class import Employee, predict
from ..services.utils.uploadfile import val_file, write_to_mysql
from .. import db
from ..services.utils import preprocess_model
from ..services.utils import submit_db

survey_bp = Blueprint('survey', __name__, template_folder='../../templates')

# Unified data storage
submission_data = {}

@survey_bp.route('/personal', methods=['GET', 'POST'])
def personal():
    if request.method == 'POST':
        # Collect data
        submission_data.update({
            'id':request.form.get('id'),
            'Gender': request.form.get('gender'),
            'Age': request.form.get('age'),
            'Relationship Status': request.form.get('relationship_status')
        })
        return redirect(url_for('survey.company'))

    return render_template('personal.html')


@survey_bp.route('/qualifications_experience', methods=['GET', 'POST'])
def qualifications_experience():
    if request.method == 'POST':
        # Append to submission_data
        submission_data.update({
            'Highest Educational Qualification': request.form.get('highest_qualification'),
            'Field of Education': request.form.get('field_of_education'),
            'Years of Working Experience': request.form.get('years_of_experience'),
            'Years within Current Domain': request.form.get('years_in_domain')
        })
        submit_db.submit_value(submission_data)
        return redirect(url_for('survey.success'))

    return render_template('qualifications_experience.html')


performance_rating_mapping = {
    'Excellent': '4',
    'Good': '3',
    'Average': '2',
    'Poor': '1'
}

@survey_bp.route('/job', methods=['GET', 'POST'])
def job():
    if request.method == 'POST':
        submission_data.update({
            'Employee code/number': request.form.get('position_role'),
            'Job type': request.form.get('job_type'),
            'Job Location': request.form.get('job_location'),
            'Seniority Level': request.form.get('seniority_level'),
            'Salary': request.form.get('salary_band'),
            'avg Hours worked per week': request.form.get('hours_per_week'),
            'Value of benefits/allowance provided': request.form.get('value_of_benefits'),
            'Performance Rating': performance_rating_mapping.get(request.form.get('performance_rating'), None),
            'Training/upskilling opportunities provided': request.form.get('training_opportunities'),
            'average Travel on work percentage': request.form.get('travel_percentage'),
            'Unpaid Overtime hours per week': request.form.get('unpaid_overtime_percentage')
        })
        return redirect(url_for('survey.work_satisfaction'))

    return render_template('job.html')


@survey_bp.route('/company', methods=['GET', 'POST'])
def company():
    if request.method == 'POST':
        submission_data.update({
            'Employee department': request.form.get('employee_department'),
            'Years in current role': request.form.get('years_in_current_role'),
            'Years with current supervisor': request.form.get('years_with_supervisor'),
            'Years since last promotion': request.form.get('years_since_last_promotion'),
            'last salary adjustment percentage': request.form.get('percentage_increase_in_salary')
        })
        return redirect(url_for('survey.job'))

    return render_template('company.html')


satisfaction_mapping = {
    'Satisfactory': 'Yes',
    'Unsatisfactory': 'No'
}

@survey_bp.route('/work_satisfaction', methods=['GET', 'POST'])
def work_satisfaction():
    if request.method == 'POST':
        submission_data.update({
            'Work-Life balance': satisfaction_mapping.get(request.form.get('work_life_balance')),
            'employer Recognition/award': satisfaction_mapping.get(request.form.get('recognition')),
            'Job satisfaction': satisfaction_mapping.get(request.form.get('job_satisfaction')),
            'Company satisfaction': satisfaction_mapping.get(request.form.get('company_satisfaction'))
        })
        return redirect(url_for('survey.qualifications_experience'))

    return render_template('work_satisfaction.html')


@survey_bp.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')


@survey_bp.route('/upload', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        file = request.files['file']
        df = val_file(file)
        if df is not None:  # Validation success
            write_to_mysql(df)
            flash("Data uploaded successfully!", "success")
            return redirect(url_for('survey.success'))
        else:
            flash("Column validation failed. Please check your file.", "danger")
    return render_template('upload.html')
