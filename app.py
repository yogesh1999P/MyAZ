import sklearn as sklearn
from flask import Flask, request, render_template, send_from_directory
import pickle
import pandas as pd
import numpy as np

app = Flask("__name__")

q = ""


df_desc=pd.read_csv("symptom_Description.csv")
df_prec=pd.read_csv("symptom_precaution.csv")
df1=pd.read_csv("Symptom-severity.csv")

@app.route("/")
def loadPage():
    return render_template('home.html', query="")


@app.route("/predict", methods=['POST'])
def predict():
    inputQuery1 = request.form.get('symptom1')
    inputQuery2 = request.form.get('symptom2')
    inputQuery3 = request.form.get('symptom3')
    inputQuery4 = request.form.get('symptom4')
    inputQuery5 = request.form.get('symptom5')


    if inputQuery1=="None" and inputQuery2=="None" and inputQuery3=="None" and inputQuery4=="None" and inputQuery5=="None":
        o1="Please select atleast one Symptom"
        o2="Please select atleast one Symptom"
    else:
        psymptoms = [inputQuery1,inputQuery2,inputQuery3,inputQuery4,inputQuery5]
        a = np.array(df1["Symptom"])
        b = np.array(df1["weight"])
        for j in range(len(psymptoms)):
            for k in range(len(a)):
                if psymptoms[j] == a[k]:
                    psymptoms[j] = b[k]

        nulls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        psy = [psymptoms + nulls]

        model = pickle.load(open("model.sav", "rb"))

        single = model.predict(psy)
        print(single)

        contain_values = df_desc[df_desc['Disease'].str.contains(single[0])]
        contain_values1 = df_prec[df_prec['Disease'].str.contains(single[0])]
        o1 = "You might be suffering from " + single[0] + ". " + contain_values.iloc[0, 1]
        o2 = contain_values1.iloc[0]


    return render_template('home.html', output1=o1, output2=o2, symtom1=request.form.get('symptom1'),
                           symtom2=request.form.get('symptom2'),symtom3=request.form.get('symptom3'),symtom4=request.form.get('symptom4'),symtom5=request.form.get('symptom5'))


if __name__ == "__main__":
    app.run()
