import sqlite3
import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def create_db_from_csv(csv_file, db_file):
  print("Creates an SQLite database from a CSV file")
  """Creates an SQLite database from a CSV file.

  Args:
    csv_file: The path to the CSV file.
    db_file: The path to the output SQLite database.
  """
  db_path = os.path.join(script_dir, db_file)
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  # Read the CSV header to create the table schema
  with open(csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

    # Create the table
    column_types = ', '.join(['{} TEXT'.format(col) for col in header])
    create_table_sql = f'CREATE TABLE data ({column_types})'
    cursor.execute(create_table_sql)

  # Insert data into the table
  with open(csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
      placeholders = ', '.join(['?'] * len(row))
      insert_sql = f'INSERT INTO data VALUES ({placeholders})'
      cursor.execute(insert_sql, row)

  conn.commit()
  conn.close()

# Example usage:
csv_file = script_dir + '\\data\\data.csv'
db_file = 'my_data.db'
create_db_from_csv(csv_file, db_file)