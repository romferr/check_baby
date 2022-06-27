import sqlalchemy

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Column, exc, Integer, String, Date, Boolean, MetaData, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)

Base = declarative_base()

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@localhost:3307/checkbaby_db")
metadata = MetaData(engine)
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


class Biberon(Base):
    __tablename__ = 'biberons'
    id = Column(Integer, primary_key=True)
    type = Column(String(16), default='Lait')
    ml = Column(Float, default=0)

    def __repr__(self):
        return f'<Post "{self.id}">'


class Care(Base):
    __tablename__ = 'cares'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    biberon_id = Column(Integer, ForeignKey('biberons.id'))
    pipi = Column(Boolean, default=False)
    selle = Column(Boolean, default=False)
    vitamine_D = Column(Boolean, default=False)
    yeux = Column(Boolean, default=False)
    nez = Column(Boolean, default=False)
    peau = Column(Boolean, default=False)
    bain = Column(Boolean, default=False)
    biberon = relationship("Biberon", back_populates="cares")

    def __repr__(self):
        return f'<Post "{self.id}">'


Biberon.cares = relationship("Care", order_by=Care.id, back_populates="biberon")
try:
    Base.metadata.create_all(engine)
except exc.SQLAlchemyError as error:
    print(f"{error.code} - {error.args}")


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        element = request.form['element']
        care_id = request.form['careId']

        care = session.query(Care).filter(Care.id == care_id).one()
        care.__setattr__(element, not care.__getattribute__(element))
        return redirect('/')
    else:
        cares = session.query(Care).order_by(Care.id).all()
        return render_template('index.html', cares=cares, )


if __name__ == '__main__':
    app.run(debug=True)
