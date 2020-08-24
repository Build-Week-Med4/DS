import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd

DF_PATH = 'data/cannabis_.csv'

DB_PATH = 'sqlite://cannabis.db'
df = pd.read_csv(DF_PATH)

db = SQLAlchemy()
migrate = Migrate()




class Strain(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    strain = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    rating = db.Column(db.Integer)
    effects = db.Column(db.String)
    flavor = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return f'ID = {self.id} Strain = {self.strain}' #Type = {self.type} Rating = {self.rating} Effects = {self.effects} Flavor = {self.flavor} Description = {self.description}'


class UserStrain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strain = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    rating = db.Column(db.Integer)
    effects = db.Column(db.String)
    flavor = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return f'ID = {self.id} Strain = {self.strain}' #Type = {self.type} Rating = {self.rating} Effects = {self.effects} Flavor = {self.flavor} Description = {self.description}'






BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "cannabis.db")


for i in range(0,len(df)):
    in_q = df.iloc[i][0]
    exists = Strain.query.filter_by(strain=df.iloc[i][0]).first()
    if not exists:
        db.session.add(Strain(strain = df.iloc[i][0],type = df.iloc[i][1],rating = df.iloc[i][2],effects = df.iloc[i][3],flavor = df.iloc[i][4],description = df.iloc[i][5]))

        db.session.commit()
    
    else:
        pass