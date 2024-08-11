import os
import sqlite3
from faker import Faker
import random
import logging

# Initialize Faker and logging
fake = Faker()
logging.basicConfig(level=logging.INFO)

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the full path for the database file in the same directory as the script
    db_path = os.path.join(script_dir, db_file)
    conn = sqlite3.connect(db_path)
    return conn

def create_table(conn):
    """Create employees table if it does not exist."""
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone_number TEXT,
            hire_date TEXT,
            job_id TEXT,
            salary REAL,
            department TEXT
        )
        ''')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_email ON employees (email);')

def generate_employee_data(num_records):
    """Generate a list of fake employee data with unique emails and standardized phone numbers."""
    employees = []
    email_set = set()  # To track unique emails
    job_ids = ['IT_PROG', 'HR_REP', 'FIN_ANALYST', 'SALES_REP']
    departments = ['IT', 'HR', 'Finance', 'Sales']
    
    while len(employees) < num_records:
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = format_phone_number(fake.phone_number())
        hire_date = fake.date_between(start_date='-10y', end_date='today').isoformat()
        job_id = random.choice(job_ids)
        salary = round(random.uniform(30000, 120000), 2)
        department = random.choice(departments)
        
        if email not in email_set:
            email_set.add(email)
            employees.append((first_name, last_name, email, phone_number, hire_date, job_id, salary, department))
    
    return employees

def format_phone_number(raw_phone):
    """Format phone number to a standard format."""
    # Remove any non-numeric characters from the raw phone number
    digits = ''.join(filter(str.isdigit, raw_phone))
    if len(digits) >= 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:10]}"
    return raw_phone

def insert_employee_data(conn, employee_data):
    """Insert employee data into the employees table."""
    with conn:
        conn.executemany('''
        INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, department)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', employee_data)

def main():
    # Define the database file name
    database = 'employees.db'
    num_records = 1000

    # Create a database connection
    conn = create_connection(database)
    
    # Create employees table
    create_table(conn)
    
    # Generate and insert fake data
    employee_data = generate_employee_data(num_records)
    insert_employee_data(conn, employee_data)
    
    logging.info(f"Inserted {len(employee_data)} records into the employees table.")
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
