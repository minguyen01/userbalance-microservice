import functools
from flask import Flask, render_template, redirect, request, session, g, flash
from sqlalchemy.orm import declarative_base
from database import *

# To run the web app in the search_app directory folder:
#> venv\Scripts\activate
#> set FLASK_APP=microservice
#> flask run

def create_app():
    # Initializes the application
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev', SESSION_TYPE='filesystem')

    # Sets up the database session
    Base = declarative_base()
    DATABASE_URI = 'postgresql://postgres:32Q39Ci3@localhost:5432/USER-BALANCE'
    engine = create_engine(DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    db_session = Session()

    @app.route('/', methods=('GET', 'POST'))
    def home_screen():    
        if request.method == 'POST':
            if request.form['submit'] == 'Add User':
                flash('Message: ' + request.form.get('adduser') + ' has been added')
                add_user(db_session, request.form.get('adduser'))
            elif request.form['submit'] == 'View Balance':
                balance = get_user_balance(db_session, request.form.get('viewbalance'))
                if (balance != None):
                    if (balance % 100 == 0 or balance % 10 == 0):
                        flash('Message: ' + request.form.get('viewbalance') + ' has a balance of $' + str(balance/100) + '0')
                    else:
                        flash('Message: ' + request.form.get('viewbalance') + ' has a balance of $' + str(balance/100))
                else:
                    flash('Message: This user does not exist')
            elif request.form['submit'] == 'Go To User':
                user = get_user(db_session, request.form.get('viewuser'))
                if (user != None):
                    session['user'] = user.username
                    return redirect('/user')
                else:
                    flash('Message: This user does not exist')
        return render_template('/home.html')

    @app.route('/user', methods=('GET', 'POST'))
    def user_screen():
        if request.method == 'POST':
            if request.form['submit'] == 'Add Transaction':
                amount = int(request.form.get('dollar') + request.form.get('cent'))
                if (request.form.get('mode') == 'CHARGE'):
                    amount = -amount
                add_transaction(db_session, session['user'], amount,
                                request.form.get('description'), 'PENDING')
                flash('Message: New Transaction has been added to ' + session['user'])
            elif request.form['submit'] == 'View Transactions':
                session['page'] = 1
                return redirect('/transaction')
            elif request.form['submit'] == 'Go to Homepage':
                return redirect('/')
        return render_template('/user.html')

    @app.route('/transaction', methods=('GET', 'POST'))
    def transaction_screen():
        if request.method == 'POST':
            if request.form['submit'] == 'Return To User':
                return redirect('/user')
            elif request.form['submit'] == 'Previous Page':
                session['page'] -= 1
            elif request.form['submit'] == 'Next Page':
                session['page'] += 1
            else:
                update_transaction_status(db_session, request.form['idsubmit'], request.form['submit'] + 'D')

        transactions = get_transactions(db_session, session['user'], session['page'] - 1)
        transactions_dict = {}
        for t in transactions:
            balance = t.amount
            if (balance % 100 == 0 or balance % 10 == 0):
                balance = str(balance/100) + '0'
            else:
                balance = str(balance/100)
            if (balance[0] == '-'):
                balance = '-$' + balance[1:]
            else:
                balance = '$' + balance
            transactions_dict[t.id] = []
            transactions_dict[t.id].append(balance)
            transactions_dict[t.id].append(t.description)
            transactions_dict[t.id].append(t.created_at.strftime('%m/%d/%Y, %H:%M:%S'))
            transactions_dict[t.id].append(str(t.status).split('.')[1])
        session['transactions'] = transactions_dict
        
        return render_template('/transaction.html', len = len(session['transactions']))

    return app
