from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from . import preprocess_model
from .db_class import Employee,predict
from ... import db
from sqlalchemy import text

def submit_value(submission_data):


    employee_data = submission_data.get('employee')
    employee_id = submission_data.get('id')  # 从 submission_data 获取 id

    try:
        if employee_data:

            employee = Employee(id=employee_id, **employee_data)
            db.session.add(employee)

            predicted_value = preprocess_model.prepare_model_and_predict(employee)
            prediction = predict(id=employee_id, possibility=predicted_value)
            db.session.add(prediction)

            try:
                db.session.commit()
                print("Data submitted successfully.")
            except Exception as e:
                print(f"Commit failure: {e}")
                db.session.rollback()

            # 验证插入结果
            if db.session.query(Employee).filter_by(id=employee_id).first() is not None:
                print("Employee data insert successful!", "success")
            else:
                print("Employee data insert failed!", "danger")

        else:
            flash("No employee data provided.", "danger")

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Insert failure: {str(e)}", "danger")