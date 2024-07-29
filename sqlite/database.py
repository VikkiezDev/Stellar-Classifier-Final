import sqlite3
import pandas as pd

# Create a connection to the SQLite database
conn = sqlite3.connect('data_release.db')

column_dtypes = {
    'objid': 'float64',
    'ra': 'float64',
    'dec': 'float64',
    'u': 'float64',
    'g': 'float64',
    'r': 'float64',
    'i': 'float64',
    'z': 'float64',
    'run': 'int64',
    'rerun': 'int64',
    'camcol': 'int64',
    'field': 'int64',
    'specobjid': 'float64',
    'class': 'object',
    'redshift': 'float64',
    'plate': 'int64',
    'mjd': 'int64',
    'fiberid': 'int64'
}



# List of CSV files and corresponding table names
csv_files = ['DR18.csv', 'DR17.csv', 'DR16.csv', 'DR15.csv']
table_names = ['dr18', 'dr17', 'dr16', 'dr15']

# Loop through the CSV files and create tables in the database
for csv_file, table_name in zip(csv_files, table_names):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(f'/home/vignesh-nadar/vikky/Projects & Skills/My Work/Project 2/Stellar Predictor/data/{csv_file}', dtype=column_dtypes)
    
    # Write the DataFrame to the SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Close the connection to the database
conn.close()
