import os, csv
from app import app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {
    'shab': {'password': 'shab'}
}

temp_data = {}

def get_jlpt_confirmed_counter():
    jlpt_confirmed_counter = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for level in ['1', '2', '3', '4', '5']:
        file_path = f"files/Confirmed/confirmed_data_N{level}.csv"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row is not None:
                    jlpt_confirmed_counter[level] = int(last_row[4])
                else:
                    jlpt_confirmed_counter[level] = 0
    
    return jlpt_confirmed_counter

def get_jlpt_counter():
    jlpt_counters = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for level in ['1', '2', '3', '4', '5']:
        file_path = f"files/registered_data_N{level}.csv"
        print(file_path)
        if os.path.exists(file_path):
            print("file exist")
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row is not None:
                    jlpt_counters[level] = int(last_row[4])
        else:
            jlpt_counters[level] = 0
        
    return jlpt_counters

def get_jlpt_special_need_count():
    jlpt_special_need_count = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for level in ['1', '2', '3', '4', '5']:
        file_path = f"files/need_assistance/registered_data_N{level}.csv"
        if os.path.exists(file_path):
            print("Path exist")
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row is not None:
                    jlpt_special_need_count[level] = int(last_row[4])
                else:
                    jlpt_special_need_count[level] = 0
        else:
            print("Don't exist", level)
    
    return jlpt_special_need_count

def get_jlpt_special_need_confirmed_count():
    jlpt_special_need_confirmed_count = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for level in ['1', '2', '3', '4', '5']:
        file_path = f"files/need_assistance/confirmed_data_N{level}.csv"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row is not None:
                    jlpt_special_need_confirmed_count[level] = int(last_row[4])
                else:
                    jlpt_special_need_confirmed_count[level] = 0
    
    return jlpt_special_need_confirmed_count


def read_csv(file_path):
    with open(file_path, 'r') as f:
        return list(csv.reader(f))

def write_csv(file_path, rows):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def write_deleted_log(file_path, row):
    with open(file_path, 'a') as f:
        f.write(','.join(row) + '\n')


def send_email():
    pass