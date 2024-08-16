import os
import sqlite3
from faker import Faker
import random

# Khởi tạo Faker
fake = Faker()

script_dir = os.path.dirname(os.path.abspath(__file__))
# Tạo đường dẫn đầy đủ cho tệp cơ sở dữ liệu trong cùng thư mục với tập lệnh
db_path = os.path.join(script_dir, 'top50queries.db')
# Tạo kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tạo bảng worker
create_table_query = '''
CREATE TABLE IF NOT EXISTS worker (
    worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    salary INTEGER,
    joining_date TEXT
);
'''

cursor.execute(create_table_query)

# Tạo dữ liệu ngẫu nhiên
def generate_random_worker_data(num_records):
    departments = ['HR', 'IT', 'Admin', 'Finance', 'Marketing']
    workers = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        department = random.choice(departments)
        salary = random.randint(50000, 200000)
        joining_date = fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
        workers.append((first_name, last_name, department, salary, joining_date))
    return workers

# Chèn dữ liệu ngẫu nhiên vào bảng worker
num_records = 50  # Số lượng bản ghi cần tạo
workers = generate_random_worker_data(num_records)

insert_data_query = '''
INSERT INTO worker (first_name, last_name, department, salary, joining_date)
VALUES (?, ?, ?, ?, ?);
'''

cursor.executemany(insert_data_query, workers)
conn.commit()

# Danh sách các câu lệnh SQL
# queries = [
#     'SELECT first_name AS WORKER_NAME FROM worker;',
#     'SELECT UPPER(first_name) FROM worker;',
#     'SELECT DISTINCT department FROM worker;',
#     'SELECT SUBSTR(first_name, 1, 3) FROM worker;',
#     'SELECT INSTR(first_name, "b") FROM worker WHERE first_name = "Amitabh";',
#     'SELECT RTRIM(first_name) FROM worker;',
#     'SELECT LTRIM(department) FROM worker;',
#     'SELECT DISTINCT department, LENGTH(department) FROM worker;',
#     'SELECT REPLACE(first_name, "a", "A") FROM worker;',
#     'SELECT CONCAT(first_name, " ", last_name) AS COMPLETE_NAME FROM worker;',
#     'SELECT * FROM worker ORDER BY first_name;',
#     'SELECT * FROM worker ORDER BY first_name ASC, department DESC;',
#     'SELECT * FROM worker WHERE first_name IN ("Vipul", "Satish");',
#     'SELECT * FROM worker WHERE first_name NOT IN ("Vipul", "Satish");',
#     'SELECT * FROM worker WHERE department LIKE "Admin%";',
#     'SELECT * FROM worker WHERE first_name LIKE "%a";',
#     'SELECT * FROM worker WHERE first_name LIKE "%a";',
#     'SELECT * FROM worker WHERE first_name LIKE "____h";',
#     'SELECT * FROM worker WHERE salary BETWEEN 100000 AND 500000;',
#     'SELECT * FROM worker WHERE strftime("%Y", joining_date) = "2014" AND strftime("%m", joining_date) = "02";',
#     'SELECT department, COUNT(*) FROM worker WHERE department = "Admin";',
#     'SELECT CONCAT(first_name, " ", last_name) FROM worker WHERE salary BETWEEN 50000 AND 100000;',
#     'SELECT department, COUNT(worker_id) AS no_of_worker FROM worker GROUP BY department ORDER BY no_of_worker DESC;',
#     'SELECT w.* FROM worker AS w INNER JOIN title AS t ON w.worker_id = t.worker_ref_id WHERE t.worker_title = "Manager";',
#     'SELECT worker_title, COUNT(*) AS count FROM title GROUP BY worker_title HAVING count > 1;',
#     'SELECT * FROM worker WHERE MOD(worker_id, 2) != 0;',
#     'SELECT * FROM worker WHERE MOD(worker_id, 2) = 0;',
#     'CREATE TABLE worker_clone AS SELECT * FROM worker;',
#     'SELECT * FROM worker_clone;',
#     'SELECT worker.* FROM worker INNER JOIN worker_clone USING (worker_id);',
#     'SELECT worker.* FROM worker LEFT JOIN worker_clone USING (worker_id) WHERE worker_clone.worker_id IS NULL;',
#     'SELECT DATE("now");',
#     'SELECT DATETIME("now");',
#     'SELECT * FROM worker ORDER BY salary DESC LIMIT 5;',
#     'SELECT * FROM worker ORDER BY salary DESC LIMIT 4, 1;',
#     'SELECT salary FROM worker wl WHERE 4 = (SELECT COUNT(DISTINCT w2.salary) FROM worker w2 WHERE w2.salary >= wl.salary);',
#     'SELECT DISTINCT salary FROM worker ORDER BY salary DESC LIMIT 3;',
#     'SELECT DISTINCT salary FROM worker wl WHERE 3 >= (SELECT COUNT(DISTINCT salary) FROM worker w2 WHERE wl.salary <= w2.salary) ORDER BY wl.salary DESC;',
#     'SELECT DISTINCT salary FROM worker wl WHERE 3 >= (SELECT COUNT(DISTINCT salary) FROM worker w2 WHERE wl.salary >= w2.salary) ORDER BY wl.salary DESC;',
#     'SELECT DISTINCT salary FROM worker wl WHERE n >= (SELECT COUNT(DISTINCT salary) FROM worker w2 WHERE wl.salary <= w2.salary) ORDER BY wl.salary DESC;',
#     'SELECT department, SUM(salary) AS depSal FROM worker GROUP BY department ORDER BY depSal DESC;',
#     'SELECT first_name, salary FROM worker WHERE salary = (SELECT MAX(salary) FROM worker);'
# ]

# # Thực thi các câu lệnh SQL
# for i, query in enumerate(queries, start=1):
#     print(f"Query {i}: {query}")
#     try:
#         cursor.execute(query)
#         results = cursor.fetchall()
#         for row in results:
#             print(row)
#     except Exception as e:
#         print(f"Error executing query {i}: {e}")

# Đóng kết nối
conn.close()
