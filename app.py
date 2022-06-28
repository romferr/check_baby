import sqlalchemy

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Column, exc, Integer, String, Date, Boolean, MetaData, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)

Base = declarative_base()

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@localhost:3307/checkbaby_db")
metadata = MetaData(engine)
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    daily_cares = relationship("DailyCare", back_populates="day")

    def __repr__(self):
        return f'<Post "{self.id}">'


class DailyCare(Base):
    __tablename__ = 'daily_cares'
    id = Column(Integer, primary_key=True)
    hour = Column(DateTime)
    # Biology              )
    type = Column(String(16))
    ml = Column(Float, default=0)
    pipi = Column(Boolean, default=False)
    selle = Column(Boolean, default=False)

    # Cares
    vitamine_D = Column(Boolean, default=False)
    yeux = Column(Boolean, default=False)
    nez = Column(Boolean, default=False)
    peau = Column(Boolean, default=False)
    bain = Column(Boolean, default=False)
    savon = Column(Boolean, default=False)
    comments = Column(String(1024))
    day_id = Column(Integer, ForeignKey('days.id'))
    day = relationship("Day", back_populates="daily_cares")

    def __repr__(self):
        return f'<Post "{self.id}">'


try:
    Base.metadata.create_all(engine)
except exc.SQLAlchemyError as error:
    print(f"{error.code} - {error.args}")


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        element = request.form['element']
        care_id = request.form['careId']

        care = session.query(DailyCare).filter(DailyCare.id == care_id).one()
        care.__setattr__(element, not care.__getattribute__(element))
        return redirect('/')
    else:
        days = session.query(Day)\
            .join(DailyCare)\
            .filter(Day.id == DailyCare.day_id)\
            .order_by(Day.id.desc())\
            .all()
        return render_template('index.html', days=days, )


if __name__ == '__main__':
    app.run(debug=True)
