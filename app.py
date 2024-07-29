import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import subprocess
import logging

# Create flask app
flask_app = Flask(__name__)
model = pickle.load(open("finalModel.pkl", "rb"))
pca = pickle.load(open("pca.pkl", "rb"))
scalar = pickle.load(open("scalar.pkl", "rb"))

data = pd.read_csv("/home/vignesh-nadar/vikky/My Work/finalProject/data/DR18.csv") 

label_mapping = {0: 'QSO', 1: 'STAR', 2: 'GALAXY'}

def launch_streamlit():
    subprocess.Popen(['streamlit', 'run', 'dashboard/dash.py', '--server.address=0.0.0.0', '--server.port=8501', '--server.headless=true'])

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods=["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = np.array(float_features).reshape(1, -1)
    ra_dec_redshift_plate_mjd_fiberid = features[:, [0, 1, 10, 8, 7, 9]]
    print(ra_dec_redshift_plate_mjd_fiberid)
    ugriz = features[:, [2, 3, 4, 5, 6]]
    pca_transformed = pca.transform(ugriz)
    print(pca_transformed)
    merged_features = np.hstack((ra_dec_redshift_plate_mjd_fiberid, pca_transformed))
    scaled_input = scalar.transform(merged_features)
    prediction = model.predict(scaled_input)[0]
    prediction_label = label_mapping[prediction]
    prediction_type = type(prediction_label).__name__ 



    # Filter the dataset to find a row that matches the predicted class
    filtered_data = data.loc[data['class'] == prediction_label, ['ra', 'dec', 'specobjid']]
    # shape = filtered_data.shape
    selected_row = filtered_data.sample(n=1)
    # shape2 = selected_row.shape



    # Extract parameters for the APIs
    ra = selected_row['ra'].values[0]
    dec = selected_row['dec'].values[0]
    specobj_id = selected_row['specobjid'].values[0]

    # Construct the API URLs
    image_url = f"http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?ra={ra}&dec={dec}&scale=0.4&height=512&width=512&opt=GO"
    spectral_url = f"http://skyserver.sdss.org/dr16/en/get/specById.asp?ID={specobj_id}"
    
    #, image_url=imaghttp://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?ra={ra}&dec={dec}&scale=0.4&height=512&width=512&opt=GO 
    #, {prediction_label}", image_url=image_url, spectral_url=spectral_url

    return render_template("index.html", prediction_text=f"The space object is {prediction_label}", image_url=image_url)

if __name__ == "__main__":
    launch_streamlit()  # Start Streamlit before running the Flask app
    flask_app.run(debug=True, host='0.0.0.0', port=5000)
