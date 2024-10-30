import pandas as pd


file_path = 'csvpath.csv'
df = pd.read_csv(file_path)

columns = df.columns

category_map = {
    'personal': ['Gender', 'Age', 'Relationship status'],
    'experment': ['Highest Educational Qualification', 'Field of Education', 'Years of working experience',
                     'Years within current field of employment'],
    'job': ['Employee code/number', 'Job type', 'Job Location', 'Seniority Level', 'Salary',
                   'avg Hours worked per week',
                   'Value of benefits/allowance provided', 'Performance Rating', 'Training/upskilling opportunities provided',
                   'Unpaid Overtime hours per week','average Travel on work percentage'],
    'company': ['Employee department', 'Years in current role', 'Years with current supervisor','number of employee in company'
                   'Years since last promotion',
                   'last salary adjustment percentage'],
    'work satisfiy': ['Work-Life balance', 'employer Recognition/award', 'Job satisfaction', 'Company satisfaction'],
    'prediction': ['possibility']
}


classified_data = {}
for category, category_columns in category_map.items():
    existing_columns = [col for col in category_columns if col in columns]

    if existing_columns:
        classified_data[category] = df[existing_columns]
        print(f"\n{category}:")
        print(classified_data[category])

for category, data in classified_data.items():
    output_file = f'classify_{category}.csv'
    data.to_csv(output_file, index=False)
