import sys

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def import_data():
    csv_file_path = '/create_data/synthetic_data.csv'
    df = pd.read_csv(csv_file_path)

    # connect the database
    # formal: 'mysql+pymysql://user:password@host:port/dbname'
    db_user = 'root'
    db_password = 'yjh383838'
    db_host = 'localhost'
    db_port = '3306'
    db_name = 'synthetic_data'

    connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    try:
        # try to connect
        engine = create_engine(connection_string)

        # test whether successful
        with engine.connect() as connection:
            print("Connection to the database was successful!")
            #connection.execute("SELECT 1")

        # write the data into database
        df.to_sql('people', con=engine, if_exists='append', index=False)
        print("Data has been successfully inserted into the database.")

    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")

import os
def export_database(output_sql_path):
    db_user = 'root'
    db_password = 'yjh383838'
    db_name = 'synthetic_data'

    # Construct the mysqldump command
    dump_command = f"mysqldump -u {db_user} -p{db_password} {db_name} > {output_sql_path}"

    try:
        # Use os.system to execute the dump command
        os.system(dump_command)
        print(f"Database has been successfully exported to {output_sql_path}.")

    except Exception as e:
        print(f"Error exporting the database: {e}")

def main():
    # if len(sys.argv)!=3:
    #     print("Usage: python app.py <csv_file_path> <table_name>")
    #
    # csv_file_path = sys.argv[1]
    # database_name = sys.argv[2]
    #import_datax()
    output_sql_path = '/create_data/exported_database.sql'
    export_database(output_sql_path)


if __name__ == '__main__':
    main()
