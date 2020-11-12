from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   session)
from dotenv import load_dotenv
# charger les variables d'environnement
load_dotenv()  # par défaut prend .env comme paramètre
from connector import connection
from get_data import get_topics, get_topic_page_data, get_claim_page_data
from encryption import encrypt, decrypt
import mysql.connector
from datetime import datetime
from time import strftime, sleep
from pprint import pprint


app = Flask(__name__)
app.secret_key = "key"
app.config['DEBUG'] = True

# curseur de base de données et connexion
cursor, conn = connection()

@app.route('/')
@app.route('/index')
def index():
    session['current_page'] = 'index'
    if 'loggedin' in session:
        return render_template('index.html', login_status='1', topics_data=get_topics())
    else:
        return render_template('index.html', login_status='0', topics_data=get_topics())

@app.route('/search-topic', methods=['GET', 'POST'])
def search_topic():
    filter_str = request.form['filter_str'].strip()
    print(filter_str)
    session['current_page'] = 'index'
    if 'loggedin' in session:
        return render_template('index.html', login_status='1', topics_data=get_topics(filter_str))
    else:
        return render_template('index.html', login_status='0', topics_data=get_topics(filter_str))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        print('logged in session...')
        return redirect(url_for('index'))
    if request.method == 'POST' and 'uname' in request.form and 'psw' in request.form:
        username = request.form['uname']
        password = request.form['psw']

        sql = """
            SELECT username, password FROM users
            WHERE username = '{username}'
        """.format(username=username)
        conn.ping(reconnect=True)
        cursor.execute(sql)
        account = cursor.fetchone()
        if len(account) != 0:
            print('Username exists')
            # verification du mots de passes
            password_db = account[1].encode('ascii')
            password_match = decrypt(password_db, password)
            if password_match:
                # Créer des données de session, nous pouvons accéder à ces données dans d'autres itinéraires

                session['loggedin'] = True
                session['username'] = account[0]
                session['current_page'] = 'index'
                # Redirection vers la page d'accueil
                print('logged in')
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))        
        else:

            # Le compte n'existe pas ou le nom d'utilisateur / mot de passe est incorrect
            return redirect(url_for('index'))
    else:
        # Afficher le formulaire de connexion avec un message (le cas échéant)
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'uname' in request.form and 'psw' in request.form:
        print('Inside registration..')
        username = request.form['uname']
        raw_password = request.form['psw']
        # cryptez d'abord le mot de passe
        password = encrypt(raw_password).decode('ascii')
        sql = """
            INSERT INTO users (username, password)
            VALUES ('{username}', '{password}')
        """.format(username=username, password=password)
        # print(sql)
        cursor.execute(sql)
        conn.commit()
        print('registered')
    # retourner render_template('index.html', login_status='0', topics_data=get_topics())
    return redirect(url_for('index'))

@app.route('/validate_user_name', methods=['POST'])
def validate_user_name():
    print('validating username....')
    user_name = request.form['username']
    sql = """
        select username 
        from users 
        where username = '{user_name}'
    """.format(user_name=user_name)
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    if data:
        print('Username is not available')
        return 'Username is not available'
    else:
        print('Username is available')
        return '1'

@app.route('/logout')
def logout():
    # Supprimer les données de session, cela déconnectera l'utilisateur
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    if 'current_page' in session:
        current_page = session['current_page']
        topic_id = session.get('topic_id', None)
        claim_id = session.get('claim_id', None)
        session.pop('current_page', None)
        session.pop('topic_id', None)
        if current_page == 'topic':
            print('logged out to topic page...')
            return redirect(url_for('topic', topic_id=topic_id))
        if current_page == 'claim':
            print('logged out to claim page...')
            return redirect(url_for('claim', claim_id=claim_id))
    print('logged out')
    # Redirection vers la page de connexion
    return redirect(url_for('index'))

@app.route('/create-topic', methods=['GET', 'POST'])
def create_topic():
    print('create-topic api called..')
    # Enregistrer le nouveau sujet dans la base de données
    if request.method == 'POST' and 'newtopic' in request.form:
        print('Inside new topic..')
        if 'loggedin' in session:
            topic_message = request.form['newtopic']
            topic_date = datetime.utcnow().isoformat()
            topic_by = session['username']
        else:
            return render_template('index.html')
        sql = """
            INSERT INTO topics (topic_message, topic_date, topic_by)
            VALUES ('{topic_message}', '{topic_date}', '{topic_by}')
        """.format(topic_message=topic_message,
                    topic_date=topic_date,
                    topic_by=topic_by
                )
        print(sql)
        cursor.execute(sql)
        conn.commit()
        print('topic created')
    return redirect(url_for('index'))

@app.route('/create-claim', methods=['GET', 'POST'])
def create_claim():
    print('create-topic api called..')
    # Enregistrer la nouvelle réclamation dans la base de données
    if request.method == 'POST' and 'newclaim' in request.form:
        print('Inside new claim..')
        if 'loggedin' in session:
            claim_message = request.form['newclaim']
            claim_date = datetime.utcnow().isoformat()
            claim_by = session['username']
            topic_id = request.form['topic_id']  
        else:
            return render_template('index.html')
        
        sql = """
            INSERT INTO claims (topic_id, claim_message, claim_date, claim_by)
            VALUES ('{topic_id}','{claim_message}', '{claim_date}', '{claim_by}')
        """.format(
            topic_id=topic_id,
            claim_message=claim_message,
            claim_date=claim_date,
            claim_by=claim_by
        )
        cursor.execute(sql)
        conn.commit()
        print('claim created')
    return redirect(url_for('topic', topic_id=topic_id))

@app.route('/topic/<topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    # définir la page actuelle de la session comme sujet
    session['current_page'] = 'topic'
    session['topic_id'] = topic_id
    login_status = '0'
    if 'loggedin' in session:
        login_status = '1'
    # obtenir des données de sujet
    data = get_topic_page_data(topic_id=int(topic_id))
    return render_template('topic.html', login_status=login_status, data=data)

@app.route('/search-claim/<topic_id>', methods=['GET', 'POST'])
def search_claim(topic_id):
    # définir la page actuelle de la session comme sujet
    session['current_page'] = 'topic'
    session['topic_id'] = topic_id
    login_status = '0'
    filter_str = request.form['filter_str'].strip()
    print(filter_str)
    if 'loggedin' in session:
        login_status = '1'
    # obtenir des données de sujet
    data = get_topic_page_data(topic_id=int(topic_id), filter=filter_str)
    return render_template('topic.html', login_status=login_status, data=data)

@app.route('/create-reply', methods=['GET', 'POST'])
def create_reply():
    print(request.form['choice'])
    # Enregistrer la nouvelle réponse dans la base de données
    if request.method == 'POST' and 'newreply' in request.form:
        print('Inside new claim..')
        if 'loggedin' in session:
            reply_message = request.form['newreply']
            reply_date = datetime.utcnow().isoformat()
            reply_by = session['username']
            reply_type = request.form['choice'] if 'choice' in request.form else ''
            claim_id = request.form['claim_id']  
        else:
            return render_template('index.html')
        
        sql = """
            INSERT INTO replies (claim_id, reply_message, reply_date, reply_by, reply_type)
            VALUES ('{claim_id}','{reply_message}', '{reply_date}', '{reply_by}', '{reply_type}')
        """.format(
            claim_id=claim_id,
            reply_message=reply_message,
            reply_date=reply_date,
            reply_by=reply_by,
            reply_type=reply_type
        )
        cursor.execute(sql)
        conn.commit()
        print('reply created')
    return redirect(url_for('claim', claim_id=claim_id))

@app.route('/claim/<claim_id>', methods=['GET', 'POST'])
def claim(claim_id):
    # définir la page actuelle de la session comme sujet
    session['current_page'] = 'claim'
    session['claim_id'] = claim_id
    login_status = '0'
    if 'loggedin' in session:
        login_status = '1'
    # obtenir des données de sujet
    data = get_claim_page_data(claim_id=int(claim_id))
    # pprint(data)
    return render_template('claim.html', login_status=login_status, data=data)

@app.route('/search-reply/<claim_id>', methods=['GET', 'POST'])
def search_reply(claim_id):
    # définir la page actuelle de la session comme sujet
    session['current_page'] = 'claim'
    session['claim_id'] = claim_id
    login_status = '0'
    filter_str = request.form['filter_str'].strip()
    if 'loggedin' in session:
        login_status = '1'
    # obtenir des données de sujet
    data = get_claim_page_data(claim_id=int(claim_id), filter=filter_str)
    return render_template('claim.html', login_status=login_status, data=data)
    
    
@app.errorhandler(404)
def page_not_found_404(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True, port=9000)
