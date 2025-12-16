import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import pickle

# Veri seti olusturma
np.random.seed(42)
veri_sayisi = 500

data = {
    'Yil': np.random.randint(2010, 2024, veri_sayisi),
    'Kilometre': np.random.randint(10000, 200000, veri_sayisi),
    'Motor_Gucu': np.random.randint(70, 200, veri_sayisi),
    'Vites': np.random.choice(['Manuel', 'Otomatik'], veri_sayisi),
    'Renk': np.random.choice(['Beyaz', 'Siyah', 'Gri', 'Kırmızı'], veri_sayisi),
    'Hasar_Kaydi': np.random.choice([0, 1000, 5000, 20000], veri_sayisi, p=[0.6, 0.2, 0.1, 0.1])
}

df = pd.DataFrame(data)

# Fiyat hesaplama
df['Fiyat'] = (
    500000 + 
    (df['Yil'] - 2010) * 80000 + 
    (df['Motor_Gucu'] * 3000) + 
    (df['Vites'].map({'Manuel': 0, 'Otomatik': 150000})) + 
    (df['Kilometre'] * -0.8) + 
    (df['Hasar_Kaydi'] * -1.5)
)
df['Fiyat'] += np.random.normal(0, 50000, veri_sayisi)
df['Fiyat'] = df['Fiyat'].clip(lower=300000)

print("Ornek Veri Seti Olusturuldu:")
df.to_csv('araba_fiyatlari_dataset.csv', index=False)
df = pd.read_csv('araba_fiyatlari_dataset.csv')

print(df.head())

# Eksik veri kontrolu
print("\nKayip Veri Kontrolu:")
print(df.isnull().sum())

# Veri on isleme
le = LabelEncoder()
df['Vites_Kod'] = le.fit_transform(df['Vites']) 

df = pd.get_dummies(df, columns=['Renk'], drop_first=True, dtype=int)
df = df.drop(['Vites'], axis=1)

print("\nVeri On Isleme Tamamlandi.")

# Backward Elimination
X = df.drop('Fiyat', axis=1)
y = df['Fiyat']

X = X.astype(float)
y = y.astype(float)

X_sabitli = sm.add_constant(X)
model_sm = sm.OLS(y, X_sabitli).fit()

print("\n--- Ilk Model Ozeti ---")

while True:
    p_values = model_sm.pvalues
    max_p = p_values.max()
    if max_p > 0.05:
        elenen_degisken = p_values.idxmax()
        if elenen_degisken == 'const':
             break
        print(f"'{elenen_degisken}' eleniyor (P-value: {max_p:.4f})")
        X = X.drop(elenen_degisken, axis=1)
        X_sabitli = sm.add_constant(X)
        model_sm = sm.OLS(y, X_sabitli).fit()
    else:
        break

print("\nBackward Elimination Tamamlandi. Kalan Ozellikler:")
print(X.columns.tolist())

# Model egitimi
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

final_model = LinearRegression()
final_model.fit(X_train, y_train)

y_pred = final_model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"\nModel Sonuclari:")
print(f"R2: {r2:.4f}")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")

# Modeli kaydet
data_to_save = {"model": final_model, "columns": X.columns.tolist()}

with open("araba_modeli.pkl", "wb") as file:
    pickle.dump(data_to_save, file)

print("\nModel 'araba_modeli.pkl' olarak kaydedildi!")