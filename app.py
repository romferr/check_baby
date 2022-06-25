import sqlalchemy

from flask import Flask, render_template, request, redirect
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@localhost:3306/checkbaby_db")

Base = declarative_base()

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


class Care(Base):
    __tablename__ = 'care'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    date = sqlalchemy.Column(sqlalchemy.DATE)
    pipi = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    selle = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    vitamine_D = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    yeux = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    nez = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    peau = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    bain = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


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
    app.run(Debug=True)
