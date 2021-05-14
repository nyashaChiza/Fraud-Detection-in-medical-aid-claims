import pandas as pd
import joblib

model =joblib.load('model & Pipeline/Classifier.pkl')
pipeline = joblib.load('model & Pipeline/pipeline.pkl')

data = [('member-name', 'Evans'), ('email', 'raskawrq@washington.edu'), ('gender', 'male'),('location', 'Harare'), ('employer', 'Mudo'), ('relationship', 'Wife'), ('patient_name', 'Jembwa'), ('patient_suffix', 677), ('patient_dob', '1/14/1992'), ('cause','Accident At Home'),('Fee Charged', 500),('membership_period', 4), ('number_of_claims', 3), ('number_of_dependants', 2)]

def classify(data):
    df = {}
    for x in data:
        df[x[0]] = x[1]
    data = pd.DataFrame(df, index=[0])
    features = pipeline.transform(data)
    prediction  = model.predict(features)
    if prediction[0] == 0:
        pred = 'Clean'
    elif prediction[0] == 1:
        pred = 'fraudulent'
    else:
        pred = 'error during classification'
    
    return pred

print('Claim Classification:', classify(data))




