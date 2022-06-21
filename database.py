from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql import func
import enum

Base = declarative_base()
DATABASE_URI = 'postgresql://postgres:32Q39Ci3@localhost:5432/USER-BALANCE'

class transaction_status(enum.Enum):
    PENDING = 1
    DECLINED = 2
    APPROVED = 3

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    amount = Column(Integer)
    new_user_balance = Column(Integer)
    description = Column(String)
    status = Column(Enum(transaction_status))
    created_at = Column(DateTime(timezone=True), default=func.now())

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    balance = Column(Integer, default=0)

def add_user(session, username):
    new_user = User(username=username)
    session.add(new_user)
    session.commit()

def add_transaction(session, username, amount, description, status):
    user = get_user(session, username)
    user.balance = user.balance + amount
    new_transaction = Transaction(username=username, amount=amount, new_user_balance=user.balance,
                                  description=description, status=status)
    session.add(new_transaction)
    session.commit()

def get_user_balance(session, username):
    return get_user(session, username).balance

def get_user(session, username):
    try:
        user = session.query(User).filter(username==username).one()
        return user
    except NoResultFound:
        print('This user does not exist')
    except MultipleResultsFound:
        print('There should not be multiple of the same usernames')
    
def create_tables(engine):
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    engine = create_engine(DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
