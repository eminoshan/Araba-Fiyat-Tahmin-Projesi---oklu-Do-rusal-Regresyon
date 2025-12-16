from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Model yukle
try:
    model_data = pickle.load(open('araba_modeli.pkl', 'rb'))
    model = model_data['model']
    model_columns = model_data['columns']
except Exception as e:
    print(f"Model yukleme hatasi: {e}")
    model = None
    model_columns = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Form verilerini al
    yil = int(request.form['Yil'])
    km = int(request.form['Kilometre'])
    hp = int(request.form['Motor_Gucu'])
    hasar = int(request.form['Hasar_Kaydi'])
    vites = request.form['Vites']
    renk = request.form['Renk']

    # Input verisi hazirla
    input_data = {col: 0 for col in model_columns}

    if 'Yil' in input_data:
        input_data['Yil'] = yil
    if 'Kilometre' in input_data:
        input_data['Kilometre'] = km
    if 'Motor_Gucu' in input_data:
        input_data['Motor_Gucu'] = hp
    if 'Hasar_Kaydi' in input_data:
        input_data['Hasar_Kaydi'] = hasar

    # Vites kodlamasi
    if 'Vites_Kod' in input_data:
        input_data['Vites_Kod'] = 1 if vites == 'Otomatik' else 0
    
    # Renk kodlamasi (one-hot)
    renk_col = f"Renk_{renk}"
    if renk_col in input_data:
        input_data[renk_col] = 1

    # Tahmin
    input_df = pd.DataFrame([input_data])[model_columns]
    prediction = model.predict(input_df)
    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text=f'Tahmini Arac Fiyati: {output:,.2f} TL')

if __name__ == "__main__":
    app.run(debug=True)