from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    import numpy as np
    import pandas as pd

    dataset = pd.read_csv('car2.csv')

    def ft(x):
        if x == 'Petrol':
            return 1
        if x == 'Diesel':
            return 0

    def trans(x):
        if x == 'Manual':
            return 1
        if x == 'Automatic':
            return 0

    def own(x):
        if x == 'First':
            return 2
        if x == 'Second':
            return 1
        if x == 'Third':
            return 0

    dataset['Fuel_Type'] = dataset['Fuel_Type'].apply(ft)
    dataset['Fuel_Type'] = dataset.Fuel_Type.astype(float)
    dataset['Transmission'] = dataset['Transmission'].apply(trans)
    dataset['Transmission'] = dataset.Transmission.astype(float)
    dataset['Owner_Type'] = dataset['Owner_Type'].apply(own)
    dataset['Owner_Type'] = dataset.Owner_Type.astype(float)

    X = dataset.iloc[:, 0:8].values
    y = dataset.iloc[:, -1].values

    # dx=pd.DataFrame(X)

    # training set and test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # fitting randomforestregression to training set
    from sklearn.ensemble import RandomForestRegressor
    reg = RandomForestRegressor(n_estimators=3000, random_state=0)
    reg.fit(X_train, y_train)

    # predict test results
    if request.method == 'POST':
        data = [0] * 8
        data[0] = request.form['exampleFormControlInput0']
        data[1] = request.form['exampleFormControlInput1']
        data[2] = request.form['exampleFormControlInput2']
        data[3] = request.form['exampleFormControlInput3']
        data[4] = request.form['exampleFormControlInput4']
        data[5] = request.form['exampleFormControlRadio0']
        data[6] = request.form['exampleFormControlRadio1']
        data[7] = request.form['exampleFormControlRadio2']
        if int(data[0]) >= 1886:
            data = pd.DataFrame([data])
            test_predictions = reg.predict(data)
            a = int(test_predictions[0])
            a = round(a, 3)
        else:
            return render_template('result.html', prediction=0)

    return render_template('result.html', prediction=a)


if __name__ == '__main__':
    app.run(debug=True)
