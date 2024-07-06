from flask import Flask, request, render_template, flash, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import json
import os
import csv


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    'shab': {'password': 'shab'}
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user = User()
        user.id = user_id
        return user
    return None

temp_data = {}


def get_jlpt_confirmed_counter():
    jlpt_confirmed_counter = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    for level in ['1', '2', '3', '4', '5']:
        file_path = f"confirmed_data_N{level}.csv"
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
        file_path = f"registered_data_N{level}.csv"
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'], strict_slashes=False)
def registration():
    if request.method == 'POST':
        temp_data['jlpt_level'] = request.form.get('jlpt_level', '')
        temp_data['test_center'] = request.form.get('test_center', '')
        temp_data['full_name'] = request.form.get('full_name', '').upper()
        temp_data['gender'] = request.form.get('gender', '')
        dob = request.form.get('dob', '')
        temp_data['dob_day'], temp_data['dob_month'], \
            temp_data['dob_year'] = dob.split('-')
        temp_data['pass_code'] = request.form.get('pass_code', '')
        temp_data['native_language'] = request.form.get('native_language', '')
        temp_data['nationality'] = request.form.get('nationality', '')
        temp_data['adress'] = request.form.get('adress', '')
        temp_data['country'] = request.form.get('country', '')
        temp_data['zip_code'] = request.form.get('zip_code', '')
        temp_data['phone_number'] = request.form.get('phone_number', '')
        temp_data['email'] = request.form.get('email', '')
        temp_data['institute'] = request.form.get('institute', '')
        temp_data['place_learn_jp'] = request.form.get('place_learn_jp', '')
        temp_data['reason_jlpt'] = request.form.get('reason_jlpt', '')
        temp_data['occupation'] = request.form.get('occupation', '')
        temp_data['occupation_details'] = request.form.get(
            'occupation_details', '')
        temp_data['media_jp'] = ''.join(choice if choice in request.form.getlist(
            'media_jp') else ' ' for choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        temp_data['communicate_teacher'] = ''.join(choice if choice in request.form.getlist(
            'communicate_teacher') else ' ' for choice in ['1', '2', '3', '4'])
        temp_data['communicate_friends'] = ''.join(choice if choice in request.form.getlist(
            'communicate_friends') else ' ' for choice in ['1', '2', '3', '4'])
        temp_data['communicate_family'] = ''.join(choice if choice in request.form.getlist(
            'communicate_family') else ' ' for choice in ['1', '2', '3', '4'])
        temp_data['communicate_supervisor'] = ''.join(choice if choice in request.form.getlist(
            'communicate_supervisor') else ' ' for choice in ['1', '2', '3', '4'])
        temp_data['communicate_colleagues'] = ''.join(choice if choice in request.form.getlist(
            'communicate_colleagues') else ' ' for choice in ['1', '2', '3', '4'])
        temp_data['communicate_CUSTOMERS'] = ''.join(choice if choice in request.form.getlist(
            'communicate_CUSTOMERS') else ' ' for choice in ['1', '2', '3', '4'])
        temp_data['jlpt_n1'] = ' ' if request.form.get(
            'jlpt_n1', '0') == '0' else request.form.get('jlpt_n1', ' ')
        temp_data['jlpt_n2'] = ' ' if request.form.get(
            'jlpt_n2', '0') == '0' else request.form.get('jlpt_n2', ' ')
        temp_data['jlpt_n3'] = ' ' if request.form.get(
            'jlpt_n3', '0') == '0' else request.form.get('jlpt_n3', ' ')
        temp_data['jlpt_n4'] = ' ' if request.form.get(
            'jlpt_n4', '0') == '0' else request.form.get('jlpt_n4', ' ')
        temp_data['jlpt_n5'] = ' ' if request.form.get(
            'jlpt_n5', '0') == '0' else request.form.get('jlpt_n5', ' ')
        temp_data['n1_result'] = request.form.get('n1_result', ' ')
        temp_data['n2_result'] = request.form.get('n2_result', ' ')
        temp_data['n3_result'] = request.form.get('n3_result', ' ')
        temp_data['n4_result'] = request.form.get('n4_result', ' ')
        temp_data['n5_result'] = request.form.get('n5_result', ' ')

        return render_template('confirm.html', form_data=temp_data)

    return render_template('registration.html')


@app.route('/confirm', methods=['POST'])
def confirm():
    jlpt_level = temp_data['jlpt_level']
    test_center = temp_data['test_center']
    full_name = temp_data['full_name']
    gender = temp_data['gender']
    dob_year = temp_data['dob_year']
    dob_month = temp_data['dob_month']
    dob_day = temp_data['dob_day']
    pass_code = temp_data['pass_code']
    native_language = temp_data['native_language']
    nationality = temp_data['nationality']
    adress = temp_data['adress']
    country = temp_data['country']
    zip_code = temp_data['zip_code']
    phone_number = temp_data['phone_number']
    email = temp_data['email']
    institute = temp_data['institute']
    place_learn_jp = temp_data['place_learn_jp']
    reason_jlpt = temp_data['reason_jlpt']
    occupation = temp_data['occupation']
    occupation_details = temp_data['occupation_details']
    media = temp_data['media_jp']
    teacher = temp_data['communicate_teacher']
    friends = temp_data['communicate_friends']
    family = temp_data['communicate_family']
    supervisor = temp_data['communicate_supervisor']
    colleagues = temp_data['communicate_colleagues']
    customers = temp_data['communicate_CUSTOMERS']
    jlpt_n1 = temp_data['jlpt_n1']
    jlpt_n2 = temp_data['jlpt_n2']
    jlpt_n3 = temp_data['jlpt_n3']
    jlpt_n4 = temp_data['jlpt_n4']
    jlpt_n5 = temp_data['jlpt_n5']
    n1_result = temp_data['n1_result']
    n2_result = temp_data['n2_result']
    n3_result = temp_data['n3_result']
    n4_result = temp_data['n4_result']
    n5_result = temp_data['n5_result']

    # Increment JLPT counter for the level
    jlpt_counters = get_jlpt_counter()
    jlpt_counters[jlpt_level] += 1

    # Process and store data as needed (e.g., write to files, send email)

    with open(f"registered_data_N{jlpt_level}.csv", 'a') as f:
        f.write(f"\"{jlpt_level.strip()}\",\"24B\",\"8210101\",\"{jlpt_level.strip()}\",\"{str(jlpt_counters[jlpt_level]).zfill(4)}\",\"{full_name.strip()}\",\"{gender.strip()}\",\"{dob_year.strip()}\",\"{dob_month.strip()}\",\"{dob_day.strip()}\",\"{pass_code.strip()}\",\"{native_language.strip()}\",\"{place_learn_jp.strip()}\",\"{reason_jlpt.strip()}\",\"{occupation.strip()}\",\"{occupation_details.strip()}\",\"{media}\",\"{teacher}\",\"{friends}\",\"{family}\",\"{supervisor}\",\"{colleagues}\",\"{customers}\",\"{jlpt_n1}\",\"{jlpt_n2}\",\"{jlpt_n3}\",\"{jlpt_n4}\",\"{jlpt_n5}\",\"{n1_result}\",\"{n2_result}\",\"{n3_result}\",\"{n4_result}\",\"{n5_result}\"\n")

    with open(f"registered_infos_N{jlpt_level}.csv", 'a') as f:
        f.write(f"\"{jlpt_counters[jlpt_level]}\",\"{jlpt_level}\",\"{test_center}\",\"{full_name}\",\"{gender}\",\"{dob_year}\",\"{dob_month}\",\"{dob_day}\",\"{pass_code}\",\"{native_language}\",\"{nationality}\",\"{adress}\",\"{country}\",\"{zip_code}\",\"{phone_number}\",\"{email}\"\n")

    # Function to send Email to the JLPT candidate
    # send_email(full_name, email)
    # Clear temporary data after processing
    temp_data.clear()

    # Render success page after confirmation
    return render_template('success.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    print("JLPT Counter :", get_jlpt_counter())
    print("JLPT Counter Confirmed :", get_jlpt_confirmed_counter())
    return render_template('dashboard.html', data=get_jlpt_counter(), data_2=get_jlpt_confirmed_counter())


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('jlpt'))  # Redirect to 'jlpt' endpoint
        else:
            error = 'Invalid username/password combination'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        logout_user()
        session.pop('logged_in', None)
        session.pop('username', None)
        return redirect(url_for('login'))

@app.route('/jlpt_data/N<level>', methods=['GET'])
def getJlptByLevel(level):
    data_file = f"registered_data_N{level}.csv"
    infor_file = f"registered_infos_N{level}.csv"
    data = []
    infor = []
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    if os.path.exists(infor_file):
        with open(infor_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                infor.append(row)
    return render_template('jlpt_data.html', infor=infor, data=data, level=level)


@app.route('/jlpt_data/all', strict_slashes=False)
def get_all_data():
    data = []
    infor = []
    for level in ['1', '2', '3', '4', '5']:
        data_file = f"registered_data_N{level}.csv"
        infor_file = f"registered_infos_N{level}.csv"
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
        if os.path.exists(infor_file):
            with open(infor_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    infor.append(row)
    return render_template('jlpt_data.html', infor=infor, data=data, level='all')

@app.route('/jlpt_confirmed_data/N<level>', methods=['GET'])
def get_confirmed_JlptByLevel(level):
    full_data = []
    full_data_file = f"full_confirmed_data_N{level}.csv"

    if os.path.exists(full_data_file):
        with open(full_data_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                full_data.append(row)

    return render_template('jlpt_confirm_data.html', data=full_data, level=level)


@app.route('/jlpt_confirmed_data/all', strict_slashes=False)
def get_confirmed_all_data():
    full_data = []
    for level in ['1', '2', '3', '4', '5']:
        full_data_file = f"full_confirmed_data_N{level}.csv"
        if os.path.exists(full_data_file):

            
            with open(full_data_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    full_data.append(row)

    return render_template('jlpt_confirm_data.html', data=full_data, level='all')

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

@app.route('/delete/<level>/<int:row_number>', methods=['POST', 'GET'], strict_slashes=False)
def delete_row(level, row_number):
    data_file = f"registered_data_N{level}.csv"
    data_file_2 = f"registered_infos_N{level}.csv"
    deleted_info = f"deleted_info_N{level}.csv"

    if os.path.exists(data_file) and os.path.exists(data_file_2):

        jlpt_counters = get_jlpt_counter()
        rows = read_csv(data_file)
        rows_2 = read_csv(data_file_2)

        if 0 < row_number <= len(rows):
            name = rows[row_number - 1][5]
            deleted_row = rows_2[row_number - 1]

            rows.pop(row_number - 1)
            rows_2.pop(row_number - 1)

            write_deleted_log(deleted_info, deleted_row)

            for i in range(row_number - 1, len(rows)):
                rows[i][4] = f"{int(rows[i][4]) - 1:04}"
                rows_2[i][0] = f"{int(rows_2[i][0]) - 1:04}"
            jlpt_counters[level] -= 1 

            new_raws = []
            for row in rows:
                row_string = ','.join([f'"{i}"' for i in row])
                print(row_string)
                new_raws.append(row_string)

            with open(data_file, 'w', newline='') as f:
                for row in new_raws:
                    f.write(row + '\n')
            
            write_csv(data_file_2, rows_2)

            flash(f"{name} deleted successfully!")
            return redirect(url_for('get_all_data'))
        else:
            flash("Invalid row number!")
            return redirect(url_for('get_all_data'))
    else:
        print("Files do not exist!")
        return redirect(url_for('get_all_data'))


@app.route('/confirm/<level>/<int:row_number>', methods=['POST', 'GET'], strict_slashes=False)
def confirm_candidate(level, row_number):
    """Route to confirme candidate
    This route read all the data from the registred data file
    copy the data into a new file, delete the data from temp file"""
    data_file = f"registered_data_N{level}.csv"
    full_data_info = f"full_confirmed_data_N{level}.csv"
    confirmed_data_file = f"confirmed_data_N{level}.csv"
    registred_data_file = f"registered_infos_N{level}.csv"
    jlpt_confirmed_counter = get_jlpt_confirmed_counter()

    if os.path.exists(data_file):
        rows = read_csv(data_file)
        info_rows = read_csv(registred_data_file)

        if 0 < row_number <= len(rows):
            confirmed_candidate = rows[row_number - 1]
            confirmed_candidate_data = info_rows[row_number - 1]

            jlpt_confirmed_counter[level] += 1
            confirmed_candidate[4] = f"{jlpt_confirmed_counter[level]:04}"


            with open(confirmed_data_file, 'a', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(confirmed_candidate)
            
            with open(full_data_info, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(confirmed_candidate_data)

            flash(f"Candidate {confirmed_candidate[5]} confirmed successfully!")

            return delete_row(level, row_number)
        else:
            flash("Invalid row number!")
            return redirect(url_for('get_all_data'))
    else:
        flash("File does not exist!")
        return redirect(url_for('get_all_data'))

@app.route('/tables')
def table():
    return render_template('tables.html', data=get_jlpt_counter(), data_2=get_jlpt_confirmed_counter())



@app.route('/chart', methods=['GET', 'POST'])
def chat():
    data_json = json.dumps(get_jlpt_counter())
    return render_template('chart.html', data=data_json)


@app.errorhandler(500)
def exception_handler(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def exception_handler(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def exception_handler(e):
    return render_template('405.html'), 405


if __name__ == '__main__':
    app.run(debug=True, port=6000)
