from faker import Faker
from datetime import datetime
import random
import csv


def generate_fake_data(quantity):
    fake_data = Faker()
    def generate_data():
        name = fake_data.name()
        birthdate = fake_data.date_of_birth(minimum_age = 18 , maximum_age= 60)
        curr_date = datetime.today()
        age = curr_date.year - birthdate.year - \
            ((curr_date.month,curr_date.day) < (birthdate.month, birthdate.day))
        salary = round(random.uniform(80000,270000)) #gets the job done ig
        return [name ,age, birthdate.strftime("%Y-%m-%d"), salary]
    employee_data = [generate_data() for data in range(quantity)]
    return employee_data
    
def get_csv(data):
    csv_file = 'data.csv'
    with open(csv_file,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name','age','date_of_birth','salary'])  #header row
        writer.writerows(data)

def clear_csv(csv_file):  # bit unnecessary but I created anyway
    with open(csv_file,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows('')


random_data = generate_fake_data(50)
get_csv(random_data)
