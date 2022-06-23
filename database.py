from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import func
import enum

# Replace the first '#' string with the master password
# Replace the second '#' string with the name of the database
DATABASE_URI = 'postgresql://postgres:########@localhost:5432/########'
Base = declarative_base()

# The possible statuses that a transaction may have
class transaction_status(enum.Enum):
    PENDING = 1
    DECLINED = 2
    APPROVED = 3

# The Transaction Schema
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Integer)
    new_user_balance = Column(Integer)
    description = Column(String)
    status = Column(Enum(transaction_status))
    created_at = Column(DateTime(timezone=True), default=func.now())

# The User Schema
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    balance = Column(Integer, default=0)

# Adds a user to the database
def add_user(session, username):
    new_user = User(username=username)
    session.add(new_user)
    session.commit()

# Adds a transaction to the database
def add_transaction(session, username, amount, description, status):
    user = get_user(session, username)
    new_transaction = Transaction(username=username, amount=amount, new_user_balance=user.balance+amount,
                                  description=description, status=status)
    session.add(new_transaction)
    session.commit()

# Changes the transaction status based on the status given and updates the user's actual balance if necessary
def update_transaction_status(session, id, status):
    transaction = get_transaction(session, id)
    current_status = str(transaction.status).split('.')[1]
    if (current_status == "PENDING"):
        if (current_status == "PENDING" and status == "APPROVED"):
            user = get_user(session, transaction.username)
            user.balance = user.balance + transaction.amount
        transaction.status = status
        session.commit()

# Returns the user's balance from the username given
def get_user_balance(session, username):
    user = get_user(session, username)
    if (user != None):
        return user.balance
    return None

# Returns a user from the username given
def get_user(session, username):
    try:
        user = session.query(User).filter(User.username==username).one()
        return user
    except NoResultFound:
        print('This user does not exist')
        return None
    except MultipleResultsFound:
        print('There should not be multiple of the same usernames')
        return None

# Returns a transaction from the id given
def get_transaction(session, id):
    try:
        transaction = session.query(Transaction).filter(Transaction.id==id).one()
        return transaction
    except NoResultFound:
        print('This transaction does not exist')
    except MultipleResultsFound:
        print('There should not be multiple of the same id')

# Returns at least ten transactions from the username given, offsetted by a page number
def get_transactions(session, username, page):
    return session.query(Transaction).filter(Transaction.username==username).order_by(Transaction.id.desc()).limit(10).offset(page * 10).all()

# Run this file to create the database tables
if __name__ == "__main__":
    engine = create_engine(DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)
