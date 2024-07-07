from flask import Flask, request, render_template, flash, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import *
import os
import csv


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    return User(user_id)


@app.route('/', strict_slashes=False)
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
        if request.form.get('needAssistance'):
            temp_data['needAssistance'] = request.form['needAssistance']
            temp_data['assistanceType'] = request.form['assistanceType']

        return render_template('confirm.html', form_data=temp_data)

    return render_template('registration.html')


@app.route('/confirm', methods=['POST'], strict_slashes=False)
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


    # Process and store data as needed (e.g., write to files, send email)
    # If Candidate need assistance, All the data will be stored in a different file
    if temp_data['needAssistance'] == 'yes':
        jlpt_counters = get_jlpt_special_need_count()
        jlpt_counters[jlpt_level] += 1
        with open(f"files/need_assistance/registered_data_N{jlpt_level}.csv", 'a') as f:
            f.write(f"\"{jlpt_level.strip()}\",\"24B\",\"8210101\",\"{jlpt_level.strip()}\",\"{str(jlpt_counters[jlpt_level]).zfill(4)}\",\"{full_name.strip()}\",\"{gender.strip()}\",\"{dob_year.strip()}\",\"{dob_month.strip()}\",\"{dob_day.strip()}\",\"{pass_code.strip()}\",\"{native_language.strip()}\",\"{place_learn_jp.strip()}\",\"{reason_jlpt.strip()}\",\"{occupation.strip()}\",\"{occupation_details.strip()}\",\"{media}\",\"{teacher}\",\"{friends}\",\"{family}\",\"{supervisor}\",\"{colleagues}\",\"{customers}\",\"{jlpt_n1}\",\"{jlpt_n2}\",\"{jlpt_n3}\",\"{jlpt_n4}\",\"{jlpt_n5}\",\"{n1_result}\",\"{n2_result}\",\"{n3_result}\",\"{n4_result}\",\"{n5_result}\"\n")

        with open(f"files/need_assistance/registered_infos_N{jlpt_level}.csv", 'a') as f:
            f.write(f"\"{jlpt_counters[jlpt_level]}\",\"{jlpt_level}\",\"{test_center}\",\"{full_name}\",\"{gender}\",\"{dob_year}\",\"{dob_month}\",\"{dob_day}\",\"{pass_code}\",\"{native_language}\",\"{nationality}\",\"{adress}\",\"{country}\",\"{zip_code}\",\"{phone_number}\",\"{email}\",\"{temp_data['assistanceType']}\"\n")
    else:    
        jlpt_counters = get_jlpt_counter()
        jlpt_counters[jlpt_level] += 1

        with open(f"files/registered_data_N{jlpt_level}.csv", 'a') as f:
            f.write(f"\"{jlpt_level.strip()}\",\"24B\",\"8210101\",\"{jlpt_level.strip()}\",\"{str(jlpt_counters[jlpt_level]).zfill(4)}\",\"{full_name.strip()}\",\"{gender.strip()}\",\"{dob_year.strip()}\",\"{dob_month.strip()}\",\"{dob_day.strip()}\",\"{pass_code.strip()}\",\"{native_language.strip()}\",\"{place_learn_jp.strip()}\",\"{reason_jlpt.strip()}\",\"{occupation.strip()}\",\"{occupation_details.strip()}\",\"{media}\",\"{teacher}\",\"{friends}\",\"{family}\",\"{supervisor}\",\"{colleagues}\",\"{customers}\",\"{jlpt_n1}\",\"{jlpt_n2}\",\"{jlpt_n3}\",\"{jlpt_n4}\",\"{jlpt_n5}\",\"{n1_result}\",\"{n2_result}\",\"{n3_result}\",\"{n4_result}\",\"{n5_result}\"\n")

        with open(f"files/registered_infos_N{jlpt_level}.csv", 'a') as f:
            f.write(f"\"{jlpt_counters[jlpt_level]}\",\"{jlpt_level}\",\"{test_center}\",\"{full_name}\",\"{gender}\",\"{dob_year}\",\"{dob_month}\",\"{dob_day}\",\"{pass_code}\",\"{native_language}\",\"{nationality}\",\"{adress}\",\"{country}\",\"{zip_code}\",\"{phone_number}\",\"{email}\"\n")
    
    # Function to send Email to the JLPT candidate
    # send_email(full_name, email)
    # Clear temporary data after processing
    temp_data.clear()

    return render_template('success.html')


@app.route('/dashboard', methods=['GET'], strict_slashes=False)
@login_required
def dashboard():
    return render_template('dashboard.html', data=get_jlpt_counter(), data_2=get_jlpt_confirmed_counter(), data_3=get_jlpt_special_need_confirmed_count(), data_4=get_jlpt_special_need_count())


# route to get JLPT data by level
@app.route('/jlpt_data/N<level>', methods=['GET'], strict_slashes=False)
@login_required
def getJlptByLevel(level):
    data_file = f"files/registered_data_N{level}.csv"
    infor_file = f"files/registered_infos_N{level}.csv"
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
@login_required
def get_all_data():
    data = []
    infor = []
    for level in ['1', '2', '3', '4', '5']:
        data_file = f"files/registered_data_N{level}.csv"
        infor_file = f"files/registered_infos_N{level}.csv"
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

# route to get JLPT data by level for special need
@app.route('/jlpt_data_special_need/N<level>', methods=['GET'], strict_slashes=False)
@login_required
def getJlptSpecialNeedByLevel(level):
    data_file = f"files/need_assistance/registered_data_N{level}.csv"
    infor_file = f"files/need_assistance/registered_infos_N{level}.csv"
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
    return render_template('jlpt_special_need_data.html', infor=infor, data=data, level=level)

@app.route('/jlpt_data_special_need/all', strict_slashes=False)
@login_required
def getJlptSpecialNeedAll():
    data = []
    infor = []
    for level in ['1', '2', '3', '4', '5']:
        data_file = f"files/need_assistance/registered_data_N{level}.csv"
        infor_file = f"files/need_assistance/registered_infos_N{level}.csv"
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
    return render_template('jlpt_special_need_data.html', infor=infor, data=data, level='all')


@app.route('/jlpt_confirmed_data/N<level>', methods=['GET'], strict_slashes=False)
@login_required
def get_confirmed_JlptByLevel(level):
    full_data = []
    full_data_file = f"files/full_confirmed_data_N{level}.csv"

    if os.path.exists(full_data_file):
        with open(full_data_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                full_data.append(row)

    return render_template('jlpt_confirm_data.html', data=full_data, level=level)


@app.route('/jlpt_confirmed_data/all', strict_slashes=False)
@login_required
def get_confirmed_all_data():
    full_data = []
    for level in ['1', '2', '3', '4', '5']:
        full_data_file = f"files/full_confirmed_data_N{level}.csv"
        if os.path.exists(full_data_file):
            with open(full_data_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    full_data.append(row)

    return render_template('jlpt_confirm_data.html', data=full_data, level='all')


@app.route('/jlpt_confirmed_special_need_data/N<level>', methods=['GET'], strict_slashes=False)
@login_required
def get_confirmed_JlptByLevel_special_need(level):
    full_data = []
    full_data_file = f"files/confirmed/full_special_need_confirmed_data_N{level}.csv"

    if os.path.exists(full_data_file):
        with open(full_data_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                full_data.append(row)

    return render_template('jlpt_confirm_data.html', data=full_data, level=level)




@app.route('/delete/<level>/<int:row_number>', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def delete_row(level, row_number):
    data_file = f"files/registered_data_N{level}.csv"
    data_file_2 = f"files/registered_infos_N{level}.csv"
    deleted_info = f"files/deleted_info_N{level}.csv"

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
@login_required
def confirm_candidate(level, row_number):
    """Route to confirme candidate
    This route read all the data from the registred data file
    copy the data into a new file, delete the data from temp file"""
    data_file = f"registered_data_N{level}.csv"
    full_data_info = f"files/full_confirmed_data_N{level}.csv"
    confirmed_data_file = f"files/Confirmed/confirmed_data_N{level}.csv"
    registred_data_file = f"files/registered_infos_N{level}.csv"
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
    return render_template('tables.html', data=get_jlpt_counter(), data_2=get_jlpt_confirmed_counter(), data_3=get_jlpt_special_need_count())


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
    app.run(debug=True, port=5000)
