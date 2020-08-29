import os
import json
import sqlite3
import pickle


import pandas as pd
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create_app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cannabis.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    
# Databse Creation
db = SQLAlchemy(app)
Migrate(app,db)



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
DF_FILEPATH = 'cannabis_.csv'
df = pd.read_csv(DF_FILEPATH)
DF_FILEPATH_2 = 'machine_learning/medical.csv'
df2 = pd.read_csv(DF_FILEPATH_2)

for i in range(0,len(df)):
    in_q = df.iloc[i][0]
    exists = Strain.query.filter_by(strain=df.iloc[i][0]).first()
    if not exists:
        db.session.add(Strain(strain = df.iloc[i][0],type = df.iloc[i][1],rating = df.iloc[i][2],effects = df.iloc[i][3],flavor = df.iloc[i][4],description = df.iloc[i][5]))

        db.session.commit()
    
    else:
        pass



# Creating Routes

@app.route('/')
def index():
    print('Visiting Home Page')
    return'HELLO_WORLD'


@app.route('/trending')
def trending():
    print('visitng home page')
    connection = sqlite3.connect(db_path)
    print("CONNECTION:", connection)

    cursor = connection.cursor()
    print("CURSOR", cursor)
    
    query = '''
    SELECT   strain, COUNT(strain) AS qty 
    FROM     user_strain
    GROUP BY strain
    ORDER BY qty DESC
    LIMIT    1;
    '''
    results= cursor.execute(query).fetchall()

    return str(results)


@app.route('/predict', methods = ['GET','POST'])

def predict():
    '''
    Returns a JSON object of the recommended strain information 
    calculated from a users flavor and effect. 

    '''
    ### Load Files
    #Load Model
    KNN_FILEPATH = 'machine_learning/knn.pkl'
    print("LOADING THE MODEL...")
    with open(KNN_FILEPATH, "rb") as model_file:
        saved_model = pickle.load(model_file)
    
    #Load Effects

    EFFECTS_FILEPATH = 'machine_learning/effects.pkl'
    print("LOADING EFFECTS..")
    with open(EFFECTS_FILEPATH, "rb") as effect_file:
        effects = pickle.load(effect_file)
    
    # Load Flavors

    FLAVOR_FILEPATH = 'machine_learning/flavors.pkl'
    print("LOADING FLAVORS...")
    with open(FLAVOR_FILEPATH, "rb") as flavors_file:
        flavors = pickle.load(flavors_file)

    
    # Load web request
    payload = request.get_json() or request.args 
    e = payload['effect']
    f = payload['flavor']

    
    ### Generate Recommendation
    # Use info to get vectors from pickled dictionaries
    effect = effects[e]
    flavor = flavors[f]

    # Generate query vector by adding these vectors
    query = effect + flavor

    # Run knn model using query vector. Needs to be reshaped
    result = saved_model.kneighbors(query.reshape(1,-1))
    DF_FILEPATH = 'cannabis_.csv'
    df = pd.read_csv(DF_FILEPATH)
    ### Get Strain names from model and locate strain information 
    strains = df.iloc[result[1][0]]['Strain'].to_list() 
    recommendation_dictionaries = []
    for i in range(2):
        rec = df[df['Strain']== strains[i]].reset_index()
        rec.columns =  ['id', 'strain', 'type','rating', 'effect', 'flavor', 'description']
        dictionary = rec.to_dict()
        recommendation_dictionaries.append(dictionary)
        db.session.add(UserStrain(strain = rec['strain'][0],type = rec['type'][0],rating = rec['rating'][0],effects = rec['effect'][0],flavor = rec['flavor'][0],description = rec['description'][0]))

        db.session.commit()

    return jsonify(recommendation_dictionaries)

@app.route('/predict_medical', methods = ['GET','POST'])

def predict_medical():
    # Load Model
    MODEL_FILEPATH = 'machine_learning/ailments_model.pkl2'
    print("LOADING THE MODEL...")
    with open(MODEL_FILEPATH, "rb") as model_file:
         saved_model = pickle.load(model_file)

    CONDITION_FILEPATH = 'machine_learning/ailments_tfidf.pkl2'
    print("LOADING CONDITIONS...")
    with open(CONDITION_FILEPATH, "rb") as conditions_file:
         conditions = pickle.load(conditions_file)

    payload = request.get_json() or request.args 
    c = payload['condition']

    # # Run knn model using query vector. Needs to be reshaped
    temp_df = saved_model.kneighbors(conditions.transform([c]).todense())[1]

    for i in range(4):
        info = df2.loc[temp_df[0][i]]['Strain']
        info_effects = df2.loc[temp_df[0][i]]['Effects']
        info_flavor = df2.loc[temp_df[0][i]]['Flavor']
        info_description = df2.loc[temp_df[0][i]]['Description']
        info_rating = df2.loc[temp_df[0][i]]['Rating']
        info_ailments = df2.loc[temp_df[0][i]]['alments']
        print(json.dumps(info))
        print(json.dumps(info_ailments))
        print(json.dumps(info_effects))
        print(json.dumps(info_flavor))
        print(json.dumps(info_description))
        print(json.dumps(info_rating))

    recommendation = {  
                        'strain':info,
                        'effects':info_effects,
                        'flavor':info_flavor,
                        'description':info_description, 
                        'rating':info_rating,
                        'ailment':info_ailments
                    }

    return jsonify(recommendation)

    

@app.route('/predict_sentence')

def predict_sentence():
    return 'TODO GET knn_model2.pkl'

#     payload = request.get_json() or request.args 
#     text = payload['text']

#     #Load Model
#     MODEL_FILEPATH = 'machine_learning/knn.pkl'
#     print("LOADING THE MODEL...")
#     with open(MODEL_FILEPATH, "rb") as model_file:
#         saved_model = pickle.load(model_file)

#     MODEL_2_FILEPATH = 'machine_learning/knn.pkl'
#     print("LOADING THE MODEL...")
#     with open(MODEL_2_FILEPATH, "rb") as model_2_file:
#         saved_model_2 = pickle.load(model_2_file)


#     temp_df = saved_model_2.kneighbors(saved_model.transform([text]).todense())[1]
    
#     for i in range(4):
#         info = df.loc[temp_df[0][i]]['strain']
#         info_effects = df.loc[temp_df[0][i]]['effects']
#         info_flavor = df.loc[temp_df[0][i]]['flavor']
#         info_description = df.loc[temp_df[0][i]]['description']
#         info_rating = df.loc[temp_df[0][i]]['rating']

#     recommendation = jsonify({'strain':info,'effects':info_effects,'flavor':info_flavor,'description':info_description, 'rating':info_rating})

#     return recommendation
     


