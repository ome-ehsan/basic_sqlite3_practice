import sqlite3
import csv
from datetime import datetime

class database:
    def __init__(self):
        self.build_connection()
        
    def build_connection(self):
        self.connection = sqlite3.connect("employees.db")
        self.cursor = self.connection.cursor()
        
    def close_connection(self):
        self.connection.close()
        
    def create_table(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    salary REAL NOT NULL 
                );
                            
                            """)
        self.connection.commit()

    def add_data(self,name,age,d_o_b,salary):

        if self.validate_date(d_o_b):
            
            months = {1:'January', 2:"February", 3:"March", 
            4:"April", 5:"may", 6:"June", 
            7:"July", 8:"August",9:"September", 
            10:"October", 11:"November", 12:"December"}
            
            dates = datetime.strptime(d_o_b,'%Y-%m-%d')
            d_o_b = f"{dates.day} {months[dates.month]}, {dates.year}"
            self.cursor.execute("INSERT INTO employees(name,age,date_of_birth,salary) VALUES (?,?,?,?);",
                                (name,age,d_o_b,salary))
            self.connection.commit()
        else:
            return "Invalid format for dates. Input date in YYYY-MM-DD format"
        
    def import_from_csv(self,csv_file):
        
        with open(csv_file,'r',newline='') as file:
            reader = csv.reader(file)
            next(reader) #skips the first row
            data = [d for d in reader]
        self.cursor.executemany("""
                    INSERT INTO employees(name,age,date_of_birth,salary)
                    VALUES (?,?,?,?);
                                """, data )    
        self.connection.commit()
        
    def validate_date(self,d_o_b):
        try:
            datetime.strptime(d_o_b,"%Y-%m-%d")
            return True
        except ValueError:
            return False 
            
    def show_data(self,data=None):   # gotta improve
        if data is not None:
            return data
        self.cursor.execute("SELECT * FROM employees;")
        return self.cursor.fetchall()
            
    def search_all(self):
        self.cursor.execute("SELECT * FROM employees;")
        data = self.cursor.fetchall()
        return data

    def search_by_name(self,name):
        self.cursor.execute("SELECT * FROM employees WHERE name = ?", (name,))
        data = self.cursor.fetchall()
        return data
    
    def search_by_age(self,age):
        self.cursor.execute("SELECT * FROM employees WHERE age = ?", (age,))
        data = self.cursor.fetchall()
        return data
    
    def search_by_salary(self,salary):
        self.cursor.execute("SELECT * FROM employees WHERE salary = ?", (salary,))
        data = self.cursor.fetchall()
        return data
    
    def search_by_namepart(self,part):
        wildcard = f"%{part}%"
        self.cursor.execute("SELECT * FROM employees WHERE name LIKE ?", (wildcard,))
        data = self.cursor.fetchall()
        return data
        
    def search_by_age_greaterthan(self,val):
        self.cursor.execute("SELECT * FROM employees WHERE age >= ?", (val,))
        data = self.cursor.fetchall()
        return data
    
    def search_by_age_lessthan(self,val):
        self.cursor.execute("SELECT * FROM employees WHERE age <= ?", (val,))
        data = self.cursor.fetchall()
        return data
        
    def search_by_salary_greaterthan(self,val):
        self.cursor.execute("SELECT * FROM employees WHERE salary >= ?", (val,))
        data = self.cursor.fetchall()
        return data
        
    def search_by_salary_leesthan(self,val):
        self.cursor.execute("SELECT * FROM employees WHERE salary <= ?", (val,))
        data = self.cursor.fetchall()
        return data
    
    def get_salary(self):
        self.cursor.execute("SELECT salary FROM employees")
        data = self.cursor.fetchall()
        return data
    
    def get_age(self):
        self.cursor.execute("SELECT age FROM employees")
        data = self.cursor.fetchall()
        return data
    
    def delete_name(self,name):
        self.cursor.execute("DELETE FROM employees WHERE name = ?;",(name,))
        self.connection.commit()
    
    def delete_age(self,age):
        self.cursor.execute("DELETE FROM employees WHERE age = ?;",(age,))
        self.connection.commit()
        
    def delete_age_lessthan(self,age):
        self.cursor.execute("DELETE FROM employees WHERE age < ?;",(age,))
        self.connection.commit()
    
    def delete_all(self):
        self.cursor.execute("DELETE FROM employees ;")
        self.connection.commit()
        
    def update_name(self,curr,new):
        self.cursor.execute("UPDATE employees SET name = ? WHERE name = ?;",(new,curr))
        self.connection.commit()  
        # return self.search_by_name(new)  
    
    def update_salary_by_age(self,new_sal,age):
        self.cursor.execute("UPDATE employees SET salary = ? WHERE age >= ?;",(new_sal,age))
        self.connection.commit() 
    
    def update_salary_by_name(self,new_sal,name):
        self.cursor.execute("UPDATE employees SET salary = ? WHERE name = ?;",(new_sal,name))
        self.connection.commit() 