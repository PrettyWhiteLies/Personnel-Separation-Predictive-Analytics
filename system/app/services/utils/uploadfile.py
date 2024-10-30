
from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
from .db_class import Employee
from sqlalchemy import inspect
from ... import db
from .preprocess_model import predict_employee_turnover
category_map_data = {
    'personal': ['Gender', 'Age', 'Relationship status'],
    'experment': ['Highest Educational Qualification', 'Field of Education', 'Years of working experience',
                  'Years within current field of employment'],
    'job': ['Employee code/number', 'Job type', 'Job Location', 'Seniority Level', 'Salary',
            'avg Hours worked per week', 'Value of benefits/allowance provided', 'Performance Rating',
            'Training/upskilling opportunities provided', 'Unpaid Overtime hours per week',
            'average Travel on work percentage'],
    'company': ['Employee department', 'Years in current role', 'Years with current supervisor',
                'number of employee in company', 'Years since last promotion', 'last salary adjustment percentage'],
    'work satisfiy': ['Work-Life balance', 'employer Recognition/award', 'Job satisfaction', 'Company satisfaction'],


}

def val_file(file):
    if not file or not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        flash("Invalid file type. Please upload a CSV or Excel file.", "danger")
        return None

    try:
        df = pd.read_csv(file) if file.filename.endswith('.csv') else pd.read_excel(file)

        all_columns = df.columns.tolist()
        missing_columns = {category: set(columns) - set(all_columns) for category, columns in category_map_data.items() if not all(col in all_columns for col in columns)}

        if missing_columns:
            for category, cols in missing_columns.items():
                print(f"Missing columns for category '{category}': {cols}", "danger")
            return None

        return df
    except Exception as e:
        flash(f"An error occurred while reading the file: {str(e)}", "danger")
        return None

def write_to_mysql(df):
    print(df.columns)

    if not inspect(db.engine).has_table('people_upload'):
        db.create_all()

    for index, row in df.iterrows():
        features = pd.DataFrame(row).T
        print("data input:",features)
        predicted_value = predict_employee_turnover(features)

        predicted=predicted_value
        employee = Employee(
            Gender=row['Gender'],
            Age=row['Age'],
            Relationship_status=row['Relationship status'],
            Highest_Educational_Qualification=row['Highest Educational Qualification'],
            Field_of_Education=row['Field of Education'],
            Years_of_Working_Experience=row['Years of working experience'],
            Years_within_Current_Domain=row['Years within current field of employment'],
            Employee_code=row['Employee code/number'],
            Job_Type=row['Job type'],
            Job_Location=row['Job Location'],
            Seniority_Level=row['Seniority Level'],
            Salary_Band=row['Salary'],
            avg_hours_worked_per_week=row['avg Hours worked per week'],
            value_of_benefits_allowance_provided=row['Value of benefits/allowance provided'],
            Performance_Rating=row['Performance Rating'],
            training_upskilling_opportunities_provided=row['Training/upskilling opportunities provided'],
            unpaid_overtime_hours_per_week=row['Unpaid Overtime hours per week'],
            average_travel_on_work_percentage=row['average Travel on work percentage'],
            Employee_Department=row['Employee department'],
            Years_in_current_role=row['Years in current role'],
            Years_with_Current_Supervisor=row['Years with current supervisor'],
            number_of_employee_in_company=row['number of employee in company'],
            Years_Since_Last_Promotion=row['Years since last promotion'],
            Percentage_Increase_in_Salary=row['last salary adjustment percentage'],
            Work_Life_Balance=row['Work-Life balance'],
            employer_recognition_award=row['employer Recognition/award'],
            Job_Satisfaction=row['Job satisfaction'],
            Company_Satisfaction=row['Company satisfaction'],
            Predicted_Label=predicted['Predicted_Label'],
            Turnover_Probability=predicted['Turnover_Probability'], # 将预测结果存储为 `possibility`
            survival_times=predicted['Estimated_Survival_Time'],
            Recommendation=predicted['Recommendation']

        )

        db.session.add(employee)


    db.session.commit()