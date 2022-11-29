import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION

def create_employee_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS employees (employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, job_id INTEGER, hire_date TEXT, salary INTEGER)")
    conn.commit()
    return cur, conn

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    json_data = json.loads(file_data)
    for i in json_data:
        cur.execute("INSERT OR IGNORE INTO employees (employee_id,first_name,last_name, job_id, hire_date, salary) VALUES (?,?,?,?,?,?)",(i["employee_id"],i["first_name"],i["last_name"],i["job_id"],i["hire_date"],i["salary"]))
    conn.commit()
    return cur, conn


# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute("SELECT hire_date, job_title FROM employees INNER JOIN jobs on employees.job_id = jobs.job_id")
    conn.commit()
    result = cur.fetchall()
    return result[0][1]


# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute("SELECT first_name, last_name FROM employees INNER JOIN jobs on employees.job_id = jobs.job_id WHERE salary < min_salary OR salary > max_salary")
    conn.commit()
    result = cur.fetchall()
    return result


# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    x = []
    y = []
    sal = []
    res = []
    other = []
    cur.execute("SELECT job_title, salary FROM employees INNER JOIN jobs on employees.job_id = jobs.job_id")
    conn.commit()
    result = cur.fetchall()
    for i in result: 
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x, y, c ="blue")
    plt.xticks(rotation=40)
    cur.execute("SELECT min_salary, max_salary, job_title FROM jobs")
    conn.commit()
    salary = cur.fetchall()
    for i in salary:
        res.append(i[2])
        sal.append(i[0])
        other.append(i[1])
    plt.scatter(res, sal, c ="red", marker = 'x')
    plt.scatter(res, other, c ="red", marker = 'x')
    plt.show()


class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)
    
    def test_visualization(self):
        visualization_salary_data(self.cur, self.conn)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

