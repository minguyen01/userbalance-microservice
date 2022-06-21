from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
DATABASE_URI = 'postgresql://postgres:32Q39Ci3@localhost:5432/USER-BALANCE'

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)

    def __repr__(self):
        return "<User(id='%s', username='%s')>" % (self.id, self.username)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)

    def __repr__(self):
        return "<User(id='%s', username='%s')>" % (self.id, self.username)

def create_tables(engine):
    Base.metadata.create_all(engine)

def add_user(session, name):
    new_user = User(username=name)
    session.add(new_user)
    session.commit()

if __name__ == "__main__":
    engine = create_engine(DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    add_user(session,"johenny")
    print("HELLO WORLD")
