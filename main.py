import logging
import psycopg2
import pandas as pd
from connectionFile import Connection

logging.basicConfig(filename='logs.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s --> %(funcName)s() --> %(message)s')


class Employee:
    # Write a Python program to list employee numbers, names and their managers and save in a xlsx file.
    def ques1(self):
        db = Connection.start_connection(self)
        cur = db.cursor()
        cur.execute("Select empno as EmployeeNumber, ename as EmployeeName,mgr as Manager from emp")
        fetch_data = cur.fetchall()
        EMP_Number =[]
        Name=[]
        Manager =[]

        for data in fetch_data:
            temp_list = list(data)
            EMP_Number.append(temp_list[0])
            Name.append(temp_list[1])
            Manager.append(temp_list[2])
        df = pd.DataFrame({'EMP_Number': EMP_Number, 'Name': Name, 'Manager': Manager})
        print(df)
        final_data = pd.ExcelWriter('/Users/sahilseli/Sigmoid/CodeSigmoid/PyCharm/assignment_python/query/query1.xlsx')
        df.to_excel(final_data, sheet_name='Q1', index=False)
        final_data.save()
        db.close()
        logging.info("Connection Closed")

    # Write a python program to list the Total compensation given till his / her last date or till now of all the employees till date in a xlsx file.
    def ques2(self):
        db = Connection.start_connection(self)
        cur = db.cursor()
        # cur.execute("UPDATE jobhist SET enddate=CURRENT_DATE WHERE enddate IS NULL;")
        data = cur.execute(
            "SELECT emp.ename, "
            "jh.empno, dept.dname, jh.deptno, "
            "ROUND((jh.enddate-jh.startdate)/30*jh.sal,0) "
            "AS total_compensation, ROUND((jh.enddate-jh.startdate)/30,0) as months_spent FROM "
            "jobhist as jh INNER JOIN dept ON jh.deptno=dept.deptno INNER JOIN emp ON jh.empno=emp.empno;")
        fetch_data = cur.fetchall()

        Employee_Name, Employee_No, Dept_Name, Dept_Number,Total_Compensation, Months_Spent = ([] for i in range(1,7))
        for data in fetch_data:
            temp_list = list(data)
            Employee_Name.append(temp_list[0])
            Employee_No.append(temp_list[1])
            Dept_Name.append(temp_list[2])
            Dept_Number.append(temp_list[3])
            Total_Compensation.append(temp_list[4])
            Months_Spent.append(temp_list[5])
        df = pd.DataFrame(
            {'Employee_Name': Employee_Name, 'Employee_No': Employee_No, 'Dept_Name': Dept_Name,
             'Dept_Number': Dept_Number, 'Total_Compensation': Total_Compensation, 'Months_Spent': Months_Spent})
        writer = pd.ExcelWriter('/Users/sahilseli/Sigmoid/CodeSigmoid/PyCharm/assignment_python/query/query2.xlsx')
        df.to_excel(writer, sheet_name='Q2', index=False)
        writer.save()
        db.close()
        logging.info("Connection Close")

   #  Read and upload the above xlsx in 2) into a new table in the Postgres DB
    def file_to_query(self, data, file):
        engine = Connection.get_engine(self)
        try:
            if data == 'Q2':
                df = pd.read_excel(file, 'Q2')
                df.to_sql(name='total_compensation', con=engine, if_exists='append', index=False)
        except:
            logging.info("Query Execution Unsuccessful")
        finally:
            logging.info("Table Creation Successful.")

    def ques3(self):
        with pd.ExcelFile('query/query2.xlsx') as xls1:
            for sheet_name in xls1.sheet_names:
                print(sheet_name)
                print(xls1)
                obj.file_to_query(sheet_name, xls1)

    #From the xlsx in 2) create another xlsx to list total compensation given at Department level till date. Columns: Dept No, Dept,Name, Compensation
    def read_sheets(self, data, file):
        try:
            if data == 'Q2':
                df = pd.read_excel(file, 'Q2')
                return df
        except:
            logging.info("Execution Unsuccessful")
        finally:
            logging.info("Execution Successful.")

    def ques4(self):
        with pd.ExcelFile('query/query2.xlsx') as xls2:
            for sheet_name in xls2.sheet_names:
                new_df = obj.read_sheets(sheet_name, xls2)

        temp1_df = new_df.groupby(['Dept_Name', 'Dept_Number']).agg(
            Total_Compensation=pd.NamedAgg(column='Total_Compensation', aggfunc="sum")).reset_index()

        final_data = pd.ExcelWriter('query/query4.xlsx')
        temp1_df.to_excel(final_data, sheet_name='Q4', index=False)
        final_data.save()

obj = Employee()
obj.ques1()
obj.ques2()
obj.ques3()
obj.ques4()