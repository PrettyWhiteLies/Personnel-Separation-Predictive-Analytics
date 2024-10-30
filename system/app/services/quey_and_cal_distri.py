from .. import db
import numpy as np

def cal_dist(data):
    grouped_data = {}
    for item in data:
        if item.label not in grouped_data:
            grouped_data[item.label] = []
        grouped_data[item.label].append(item.Salary)

    results = {}  #
    for label, values in grouped_data.items():
        values.sort()
        q1 = np.percentile(values, 25)
        q2 = np.percentile(values, 50)
        q3 = np.percentile(values, 75)
        results[label] = (q1, q2, q3)
    return results
class Employee(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)

    # Personal Information
    Gender = db.Column(db.Enum('Male', 'Female', 'Other'), name='Gender')
    Age = db.Column(db.Integer, name='Age')
    Relationship_status = db.Column(db.Enum('Single', 'Married', 'De-facto', 'Divorced'),
                                    name='Relationship status')

    # Qualifications and Experience
    Highest_Educational_Qualification = db.Column(db.Enum('School', 'Undergraduate', 'Post-graduate', 'Doctorate'),
                                                  name='Highest Educational Qualification')
    Field_of_Education = db.Column(
        db.Enum('Life Sciences', 'Medical', 'Other', 'Human Resources', 'Marketing', 'Technical Degree'),
        name='Field of Education')
    Years_of_Working_Experience = db.Column(db.Integer, name='Years of working experience')
    Years_within_Current_Domain = db.Column(db.Integer, name='Years within current field of employment')

    # Job Information
    Employee_code = db.Column(db.Integer, name='Employee code/number')
    Job_Type = db.Column(db.Enum('Permanent', 'Fixed-term', 'Contract', 'Casual/adhoc'), name='Job type')
    Job_Location = db.Column(db.Enum('On-Site', 'Remote', 'Hybrid'), name='Job Location')
    Seniority_Level = db.Column(db.Enum('Graduate', 'Junior', 'Mid', 'Senior', 'Executive'), name='Seniority Level')
    Salary_Band = db.Column(db.Numeric(10, 2), name='Salary')
    avg_hours_worked_per_week = db.Column(db.Numeric(4, 2), name='avg Hours worked per week')
    value_of_benefits_allowance_provided = db.Column(db.Numeric(10, 2), name='Value of benefits/allowance provided')
    Performance_Rating = db.Column(db.Integer, name='Performance Rating')
    training_upskilling_opportunities_provided = db.Column(
        db.Enum('strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree'),
        name='Training/upskilling opportunities provided')
    average_travel_on_work_percentage = db.Column(db.Numeric(5, 2), name='average Travel on work percentage')
    unpaid_overtime_hours_per_week = db.Column(db.Numeric(5, 2), name='Unpaid Overtime hours per week')

    # Company Information
    Employee_Department = db.Column(db.Enum('Operations', 'Management', 'HR', 'Finance', 'Technical'),
                                    name='Employee department')
    Years_in_current_role = db.Column(db.Integer, name='Years in current role')
    Years_with_Current_Supervisor = db.Column(db.Integer, name='Years with current supervisor')
    Years_Since_Last_Promotion = db.Column(db.Integer, name='Years since last promotion')
    number_of_employee_in_company = db.Column(db.Integer, name='number of employee in company')
    Percentage_Increase_in_Salary = db.Column(db.Numeric(5, 2), name='last salary adjustment percentage')

    # Work Satisfaction
    Work_Life_Balance = db.Column(db.Enum('strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree'),
                                  name='Work-Life balance')
    employer_recognition_award = db.Column(
        db.Enum('strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree'),
        name='employer Recognition/award')
    Job_Satisfaction = db.Column(db.Enum('strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree'),
                                 name='Job satisfaction')
    Company_Satisfaction = db.Column(db.Enum('strongly disagree', 'disagree', 'neutral', 'agree', 'strongly agree'),
                                     name='Company satisfaction')

    Label = db.Column(db.Float, name='Label')

    def calculate_distribution_salary(self):
        data = db.session.query(Employee.label, Employee.Salary_Band).all()  # 只读取 label 和 Salary

        return cal_dist(data)

    def calculate_distribution_Age(self):
        data = db.session.query(Employee.label, Employee.Age).all()
        return cal_dist(data)
    def calculate_distribution_work(self):

        data = db.session.query(Employee.label, Employee.Years_of_Working_Experience).all()
        return cal_dist(data)

    def calculate_distribution_avg_work(self):
        data = db.session.query(Employee.label, Employee.avg_hours_worked_per_week).all()
        return cal_dist(data)

class predict(db.Model):
    __tablename__ = 'Prediction'
    id = db.Column(db.Integer, primary_key=True)
    possibility = db.Column(db.Numeric(10, 2))

