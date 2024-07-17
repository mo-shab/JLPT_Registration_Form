from flask import Flask, request, render_template, flash, url_for, redirect, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config import *
from logging import FileHandler, WARNING
import os
from flask_mail import Mail, Message
import csv
import logging
import smtplib


app = Flask(__name__)
app.secret_key = 'This_Is_Not_My_Secret_Key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

file_hundler = FileHandler('errorlog.txt')
file_hundler.setLevel(WARNING)
app.logger.addHandler(file_hundler)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {
    'shab': {'password': 'shab'}
}


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


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
        temp_data['needAssistance'] = request.form['needAssistance']

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
            f.write(f"\"{jlpt_counters[jlpt_level]}\",\"{jlpt_level}\",\"{test_center}\",\"{full_name}\",\"{gender}\",\"{dob_year}\",\"{dob_month}\",\"{dob_day}\",\"{pass_code}\",\"{native_language}\",\"{nationality}\",\"{adress}\",\"{country}\",\"{zip_code}\",\"{phone_number}\",\"{email}\"\n")
    else:    
        jlpt_counters = get_jlpt_counter()
        jlpt_counters[jlpt_level] += 1

        with open(f"files/registered_data_N{jlpt_level}.csv", 'a') as f:
            f.write(f"\"{jlpt_level.strip()}\",\"24B\",\"8210101\",\"{jlpt_level.strip()}\",\"{str(jlpt_counters[jlpt_level]).zfill(4)}\",\"{full_name.strip()}\",\"{gender.strip()}\",\"{dob_year.strip()}\",\"{dob_month.strip()}\",\"{dob_day.strip()}\",\"{pass_code.strip()}\",\"{native_language.strip()}\",\"{place_learn_jp.strip()}\",\"{reason_jlpt.strip()}\",\"{occupation.strip()}\",\"{occupation_details.strip()}\",\"{media}\",\"{teacher}\",\"{friends}\",\"{family}\",\"{supervisor}\",\"{colleagues}\",\"{customers}\",\"{jlpt_n1}\",\"{jlpt_n2}\",\"{jlpt_n3}\",\"{jlpt_n4}\",\"{jlpt_n5}\",\"{n1_result}\",\"{n2_result}\",\"{n3_result}\",\"{n4_result}\",\"{n5_result}\"\n")

        with open(f"files/registered_infos_N{jlpt_level}.csv", 'a') as f:
            f.write(f"\"{jlpt_counters[jlpt_level]}\",\"{jlpt_level}\",\"{test_center}\",\"{full_name}\",\"{gender}\",\"{dob_year}\",\"{dob_month}\",\"{dob_day}\",\"{pass_code}\",\"{native_language}\",\"{nationality}\",\"{adress}\",\"{country}\",\"{zip_code}\",\"{phone_number}\",\"{email}\"\n")
    
    # Function to send Email to the JLPT candidate
    msg_body = f"""Chère {full_name},
            Nous vous remercions de votre inscription au JLPT 2024 qui aura lieu le 1 décembre 2024 à Rabat. Vous avez 48h pour effectuer le paiement de votre inscription au Niveau N{jlpt_level} sinon elle sera supprimée et vous devrez recommencer.
       
      Le Passcode que vous avez choisi est : {pass_code} Gardez le en lieu sure.
      
            Le paiement doit se faire sur le compte de l'Association Marocaine pour la Langue et la Culture Japonaise dont les coordonnées bancaires sont les suivantes :
            AWB succursale FAR Casablanca
            RIB : 007 780 0002 372 000 308 926 94
            CODE SWIFT : BCMAMAMC
            rappel du prix de l'inscription : 
            N1 : 450 DH.
            N2 : 400 DH.
            N3 : 350 DH.
            N4 : 300 DH.
            N5 : 250 DH.
       
            Nous vous prions de nous envoyer le reçu de paiement et une photo d'identité (voir spécificités plus bas) au maximum 48h après votre inscription sur l'adresse mail suivante : jlpt@amlcj.ma en indiquant vos nom et prénom et le Niveau JLPT que vous souhaitez passer.

            Un email de confirmation vous sera envoyé. Vous recevrez votre convocation au plus tard 15 jours après la fin des inscriptions soit au plus tard le 10 septembre.
 
            Si passé ce délai vous n'avez pas encore reçu votre convocation, nous vous prions de nous contacter sur l'adresse email : jlpt@amlcj.ma
     Spécificité de la photo d'identité à scanner :
           
                3 ～ 4 cm de haut × 3 cm de large
                Pris au cours des 6 derniers mois
                Peut être en noir et blanc ou en couleur
                Peut être pris avec un appareil photo numérique
                Photos sans bordure
           
      
            Vous devrez coller la même photo originale, imprimée sur papier photo, sur la convocation qui vous sera envoyée.
      
           Photos à éviter :
                Photos plus grandes ou plus petites que 3～4cm × 3cm
                Prise sur un fond non uni (fond sombre)
                Photos floues (trop sombres)
                Yeux fermés
                Vous portez un chapeau
                Vous portez des lunettes de soleil
                Vos mains sont sur les photos
                Snapshots, tels que ceux pris avec d'autres personnes
               Visage trop petit ou trop grand par rapport à la taille de la photo
                Photocopies couleur
           
        Gambatte kudasai!!
         Dear {full_name},
        Thank you for registering for the JLPT 2024 which will take place on December 1 in Rabat.
       The passcode you have chosen is: {pass_code}, Please keep it safe.
       
            You have 48 hours to make payment for your Level N{jlpt_level} registration, otherwise it will be deleted and you will have to start over.
      
            Payment must be made to the account of the Moroccan Association for Japanese Language and Culture whose bank details are as follows:
       
            AWB branch FAR Casablanca
            Bank details: 007 780 0002 372 000 308 926 94
            SWIFT CODE: BCMAMAMC

            Reminder of the registration fee:
                N1: 450 DH.
                N2: 400 DH.
                N3: 350 DH.
                N4: 300 DH.
                N5: 250 DH.
        
            Please send us the payment receipt and a photo ID (see specifics below) no later than 48 hours after your registration to the following email address: <a href="mailto:jlpt@amlcj.ma">jlpt@amlcj.ma</a> indicating your first and last name and the JLPT Level that you want to pass.
       
            A confirmation email will be sent. You will receive your voucher no later than 15 days after the end of registration, i.e. no later than September 10.
       
            If after this period you have not yet received your voucher, please contact us on the email address: <a href="mailto:jlpt@amlcj.ma">jlpt@amlcj.ma</a>.
       
            Specificity of ID photo to be scanned:
                3～4cm high × 3cm wide
                Took within the last 6 months
                Can be black and white or color
                Can be taken with a digital camera
                Borderless photos
      
            You will have to paste the same original photo, printed on photo paper, on the invitation that will be sent to you.
        
            ictures to avoid:
                Photos larger or smaller than 3～4cm × 3cm
                Taken against a non-plain background (dark background)
                Blurry photos (too dark)
                Eyes closed
                You wear a hat
                You wear sunglasses
                Your hands are in the photos
                Snapshots, such as those taken with other people
                Face too small or too big for photo size
                Color photocopies
           
        Gambatte kudasai!!
"""
    
    html_body = f"""
<html>
    <head></head>
    <body>
        <p>Chère <strong>{full_name}</strong>,</p>
        <p>
            Nous vous remercions de votre inscription au <b>JLPT 2024</b> qui aura lieu le 1 décembre 2024 à Rabat. Vous avez 48h pour effectuer le paiement de votre inscription au Niveau <b>N{jlpt_level}</b> sinon elle sera supprimée et vous devrez recommencer.
        </p>
        <p> Le Passcode que vous avez choisi est : <b>{pass_code}</b> Gardez le en lieu sure.</p>
        <p>
            Le paiement doit se faire sur le compte de l'Association Marocaine pour la Langue et la Culture Japonaise dont les coordonnées bancaires sont les suivantes :
        </p>
        <p>
            <b>AWB succursale FAR Casablanca</b><br>
            <b>RIB :</b> 007 780 0002 372 000 308 926 94<br>
            <b>CODE SWIFT :</b> BCMAMAMC
        </p>
        <p> rappel du prix de l'inscription : </p>
        <p>
            <ul>
                <li>N1 : 450 DH.</li>
                <li>N2 : 400 DH.</li>
                <li>N3 : 350 DH.</li>
                <li>N4 : 300 DH.</li>
                <li>N5 : 250 DH.</li>
            </ul>
        <p>
            Nous vous prions de nous envoyer le reçu de paiement et une photo d'identité (voir spécificités plus bas) au maximum 48h après votre inscription sur l'adresse mail suivante : <a href="mailto:jlpt@amlcj.ma">jlpt@amlcj.ma</a> en indiquant vos nom et prénom et le Niveau JLPT que vous souhaitez passer.
        </p>
        <p>
            Un email de confirmation vous sera envoyé. Vous recevrez votre convocation au plus tard 15 jours après la fin des inscriptions soit au plus tard le 15 Aout.
        </p>
        <p>
            Si passé ce délai vous n'avez pas encore reçu votre convocation, nous vous prions de nous contacter sur l'adresse email : <a href="mailto:jlpt@amlcj.ma">jlpt@amlcj.ma</a>.
        </p>
        <p>
            <b>Spécificité de la photo d'identité à scanner :</b><br>
            <ul>
                <li>3 ～ 4 cm de haut × 3 cm de large</li>
                <li>Pris au cours des 6 derniers mois</li>
                <li>Peut être en noir et blanc ou en couleur</li>
                <li>Peut être pris avec un appareil photo numérique</li>
                <li>Photos sans bordure</li>
            </ul>
        </p>
        <p>
            Vous devrez coller la même photo originale, imprimée sur papier photo, sur la convocation qui vous sera envoyée.
        </p>
        <p>
            <b>Photos à éviter :</b><br>
            <ul>
                <li>Photos plus grandes ou plus petites que 3～4cm × 3cm</li>
                <li>Prise sur un fond non uni (fond sombre)</li>
                <li>Photos floues (trop sombres)</li>
                <li>Yeux fermés</li>
                <li>Vous portez un chapeau</li>
                <li>Vous portez des lunettes de soleil</li>
                <li>Vos mains sont sur les photos</li>
                <li>Snapshots, tels que ceux pris avec d'autres personnes</li>
                <li>Visage trop petit ou trop grand par rapport à la taille de la photo</li>
                <li>Photocopies couleur</li>
            </ul>
        </p>
        <p>Gambatte kudasai!!</p>
        <p> Dear <strong>{full_name}</strong>,</p>
        <p>Thank you for registering for the JLPT 2024 which will take place on December 1 in Rabat.</p>
        <p>The passcode you have chosen is: {pass_code}, Please keep it safe.</p>
        <p>
            You have 48 hours to make payment for your Level <b>N{jlpt_level}</b> registration, otherwise it will be deleted and you will have to start over.
        </p>
        <p>
            Payment must be made to the account of the Moroccan Association for Japanese Language and Culture whose bank details are as follows:
        </p>
        <p>
            <b>AWB branch FAR Casablanca</b><br>
            <b>Bank details:</b> 007 780 0002 372 000 308 926 94<br>
            <b>SWIFT CODE:</b> BCMAMAMC
        </p>
        <p>Reminder of the registration fee:</p>
        <p>
            <ul>
                <li>N1 : 450 DH.</li>
                <li>N2 : 400 DH.</li>
                <li>N3 : 350 DH.</li>
                <li>N4 : 300 DH.</li>
                <li>N5 : 250 DH.</li>
            </ul>
        </p>
        <p>
            Please send us the payment receipt and a photo ID (see specifics below) no later than 48 hours after your registration to the following email address: <a href="mailto:jlpt@amlcj.ma">jlpt@amlcj.ma</a> indicating your first and last name and the JLPT Level that you want to pass.
        </p>
        <p>
            A confirmation email will be sent. You will receive your voucher no later than 15 days after the end of registration, i.e. no later than August 15.
        </p>
        <p>
            If after this period you have not yet received your voucher, please contact us on the email address: <a href="mailto:jlpt@amlcj.ma">jlpt@amlcj.ma</a>.
        </p>
        <p>
            <b>Specificity of ID photo to be scanned:</b><br>
            <ul>
                <li>3～4cm high × 3cm wide</li>
                <li>Took within the last 6 months</li>
                <li>Can be black and white or color</li>
                <li>Can be taken with a digital camera</li>
                <li>Borderless photos</li>
            </ul>
        </p>
        <p>
            You will have to paste the same original photo, printed on photo paper, on the invitation that will be sent to you.
        </p>
        <p>
            <b>Pictures to avoid:</b><br>
            <ul>
                <li>Photos larger or smaller than 3～4cm × 3cm</li>
                <li>Taken against a non-plain background (dark background)</li>
                <li>Blurry photos (too dark)</li>
                <li>Eyes closed</li>
                <li>You wear a hat</li>
                <li>You wear sunglasses</li>
                <li>Your hands are in the photos</li>
                <li>Snapshots, such as those taken with other people</li>
                <li>Face too small or too big for photo size</li>
                <li>Color photocopies</li>
            </ul>
        </p>
        <p>Gambatte kudasai!!</p>
    </body>
</html>
"""

    send_email(email, msg_body, html_body)
    # Clear temporary data after processing
    temp_data.clear()

    return render_template('success.html')


@app.route('/dashboard', methods=['GET'], strict_slashes=False)
@login_required
def dashboard():
    return render_template('dashboard.html', data=get_jlpt_counter(), data_2=get_jlpt_confirmed_counter(), data_3=get_jlpt_special_need_confirmed_count(), data_4=get_jlpt_special_need_count())


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
    full_data_file = f"files/need_assistance/confirmed/full_confirmed_data_N{level}.csv"

    if os.path.exists(full_data_file):
        with open(full_data_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                full_data.append(row)

    return render_template('jlpt_confirm_data.html', data=full_data, level=level)

@app.route('/jlpt_confirmed_special_need_data/all', strict_slashes=False)
@login_required
def get_confirmed_special_need_all_data():
    full_data = []
    for level in ['1', '2', '3', '4', '5']:
        full_data_file = f"files/need_assistance//confirmed/full_confirmed_data_N{level}.csv"
        if os.path.exists(full_data_file):
            with open(full_data_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    full_data.append(row)

    return render_template('jlpt_special_need_data.html', data=full_data, level='all')


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
        flash("Files do not exist!")
        return redirect(url_for('get_all_data'))


@app.route('/confirm/<level>/<int:row_number>', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def confirm_candidate(level, row_number):
    """Route to confirme candidate
    This route read all the data from the registred data file
    copy the data into a new file, delete the data from temp file"""
    data_file = f"files/registered_data_N{level}.csv"
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
    return render_template('tables.html', data=get_jlpt_counter(), data_2=get_jlpt_confirmed_counter(), data_3=get_jlpt_special_need_count(), data_4=get_jlpt_special_need_confirmed_count())


#@app.errorhandler(500)
#def exception_handler(e):
#    return render_template('500.html'), 500


@app.errorhandler(404)
def exception_handler(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def exception_handler(e):
    return render_template('405.html'), 405



@app.route('/confirm_special_need/<level>/<int:row_number>', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def confirm_special_need_candidate(level, row_number):
    data_file = f"files/need_assistance/registered_data_N{level}.csv"
    full_data_info = f"files/need_assistance/confirmed/full_confirmed_data_N{level}.csv"
    confirmed_data_file = f"files/need_assistance/confirmed/confirmed_special_need_data_N{level}.csv"
    registred_data_file = f"files/need_assistance/registered_infos_N{level}.csv"
    jlpt_confirmed_counter = get_jlpt_special_need_confirmed_count()

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

            print(f"Candidate {confirmed_candidate[5]} confirmed successfully!")

            return delete_special_need_row(level, row_number)
        else:
            print("Invalid row number!")
            return redirect(url_for('getJlptSpecialNeedAll'))
    else:
        print("File does not exist!")
        return redirect(url_for('getJlptSpecialNeedAll'))


@app.route('/delete_special_need/<level>/<int:row_number>', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def delete_special_need_row(level, row_number):
    data_file = f"files/need_assistance/registered_data_N{level}.csv"
    data_file_2 = f"files/need_assistance/registered_infos_N{level}.csv"
    deleted_info = f"files/need_assistance/deleted_info_N{level}.csv"

    if os.path.exists(data_file) and os.path.exists(data_file_2):
        print("Path found")

        jlpt_counters = get_jlpt_special_need_count()
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
                new_raws.append(row_string)

            with open(data_file, 'w', newline='') as f:
                for row in new_raws:
                    f.write(row + '\n')
            
            write_csv(data_file_2, rows_2)

            flash(f"{name} deleted successfully!")
            return redirect(url_for('getJlptSpecialNeedAll'))
        else:
            flash("Invalid row number!")
            return redirect(url_for('getJlptSpecialNeedAll'))
    else:
        flash("Files do not exist!")
        return redirect(url_for('getJlptSpecialNeedAll'))


@app.route('/download/csv/N<level>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def download_csv(level):
    file_path = f"files/Confirmed/confirmed_data_N{level}.csv"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return render_template('404.html'), 404
    
@app.route('/download_special/csv/N<level>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def download_special_need_csv(level):
    file_path = f"files/need_assistance/confirmed/confirmed_special_need_data_N{level}.csv"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return render_template('404.html'), 404

@app.route('/download', methods=['GET'], strict_slashes=False)
@login_required
def download():
    return render_template('download.html')


# Configuration settings
app.config['MAIL_SERVER'] = 'mail.amlcj.ma'  # Replace with your mail server
app.config['MAIL_PORT'] = 587  # Common port for SMTP
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USE_SSL'] = False  # Do not use SSL if using TLS
app.config['MAIL_USERNAME'] = 'jlpt@amlcj.ma'  # Your email username
app.config['MAIL_PASSWORD'] = 'Loe7WdxabmbjNmt'  # Your email password

# Initialize the Mail object
mail = Mail(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the send_email function
def send_email(email, msg_body, html_body):
    sender = 'jlpt@amlcj.ma'
    msg = Message('JLPT Inscription', sender=sender, recipients=[email])
    msg.body = msg_body
    msg.html = html_body
    
    for attempt in range(3):  # Try up to 3 times
        try:
            mail.send(msg)
            logger.info("Email sent successfully.")
            return
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
        except smtplib.SMTPConnectError as e:
            logger.error(f"Connection error: {e}")
        except smtplib.SMTPServerDisconnected as e:
            logger.error(f"Server unexpectedly closed the connection: {e}")
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
    
    logger.error("Failed to send email after 3 attempts.")


if __name__ == '__main__':
    app.run(port=5000)
